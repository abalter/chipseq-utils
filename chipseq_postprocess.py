#!/usr/bin/env python

import yaml
import json
import pandas as pd
import os
import errno
import string
import subprocess


class ChipSeqConfiguration():

    ### __init__ ###
    def __init__(self,  config_filename=""):
        with open(config_filename, 'r') as configfile:
            self.config = yaml.load(configfile)
        self.directories = self.config["Directories"]
        self.samples = self.config["Samples"]
        self.treatments = self.samples["treatments"]
        self.targets = self.samples["targets"]
        self.mockname = self.samples["mockname"]
        self.inputname = self.samples["inputname"]
        self.all_treatments = self.treatments + [self.mockname]
        self.all_targets = self.targets + [self.inputname]
        self.libraries = self.config["Libraries"]

        condorpath = self.directories["condor"]["basedir"] + "/" + self.directories["condor"]["local"]
        self.condor_command = \
            string.Template(
                "$chipseqtools/$condor_submit_list $chipseqtools/master.sh $condorpath/$jobname $command_file_name"
                )
        self.condor_command = string.Template(
            self.condor_command.safe_substitute(
                chipseqtools=self.libraries["chipseqtools"],
                condor_submit_list=self.libraries["condor_submit_list"],
                condorpath=condorpath
                )
            )

        self.intersect_command = string.Template("bedops -i $peaks_files > $intersect_file")
        comment = """
        self.coverage_command = string.template(
            "bedtools multicov -bams {bamfiles} -bed {bedfile} "\
            + "| awk '''BEGIN {{print \"\"{header}\"\"}} {{print $0}}''' > {coverage_file}"
        """

        calc_fold = "" \
            + self.config["Libraries"]["chipseqtools"] \
            + "/" \
            + self.config["Libraries"]["calc_fold"] \
            + " -n $num_treatments" \
            + " -avg log2"

        self.coverage_command = string.Template(
            "bedtools multicov -bams $bamfiles -bed $bedfile | " + calc_fold + " > $coverage_file"
            )

        self.cross_treatments = []
        for treatment in self.treatments:
            self.cross_treatments.append(treatment + "_vs_" + self.mockname)
            self.cross_treatments.append(self.mockname + "_vs_" + treatment)

        ### Make directories if they don't exist
        for feature in self.directories.keys():
            path = self.getFullPath(feature)
            try:
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

    ### /__init__ ###


    ### Unused
    def generateCommandFiles(self):
        # print(str(self.config))
        # print(json.dumps(self.config, indent=2))
        pass
    ######


    ### writeIntersectCommands ###
    def writeIntersectCommands(self, command_filename=""):
        # print("writeIntersectCommands")
        peaksdir = self.getFullPath("peaks")
        intersect_commands_file = open(command_filename, 'w')
        for treatment in self.all_treatments + self.cross_treatments:
            for target in self.targets:
                # print("target: " + target + " treatment: " + treatment)
                peaks_files = [self.getPeakSample(
                    treatment=treatment,
                    target=target,
                    rep=rep
                    ) for rep in self.samples["reps"]]
                #print(str(peaks_files))
                intersect_file = self.getIntersectFilename(
                    treatment=treatment, target=target)

                cmd = "intersectBed -wb -a " + peaks_files[0] +" -b " + peaks_files[1]
                for index in range(2,len(peaks_files)):
                    cmd += " | intersectBed -wb -a - -b " + peaks_files[index]

                cmd += " > " + intersect_file
                #print(cmd)

                comment = """
                intersect_command = self.intersect_command.substitute(
                        peaks_files=" ".join(peaks_files),
                        intersect_file=intersect_file
                        )
                """

                intersect_commands_file.write(cmd + "\n")

        intersect_commands_file.close()
    ### /writeIntersectCommands ###

    ### /writeCoverageCommands ###
    def writeCoverageCommands(self, command_filename=""):
        ### These are only for the intersected peak bed files.command_filename
        ### The peak caller calculates the coverage on the single rep peaks.

        ### Need both can do input and treated at the same time for all
        ### to make it easier to calculate coverage later.

        # print("writeCoverageCommands")
        peaksdir = self.getFullPath("peaks")
        coverage_commands_file = open(command_filename, 'w')

        ### By sample
        for treatment in self.all_treatments:
            for target in self.targets:
                # print("target: " + target + " treatment: " + treatment)

                bamfiles = [self.getBamSample(
                    treatment=treatment,
                    target=target,
                    rep=rep,
                    ) for rep in self.samples["reps"]]
                bamfiles += [self.getBamSample(
                    treatment=treatment,
                    target=self.inputname,
                    rep=rep,
                    ) for rep in self.samples["reps"]]

                samples = ["_".join([treatment, target, rep]) for rep in self.samples["reps"]]
                samples += ["_".join([treatment, self.inputname, rep]) for rep in self.samples["reps"]]
                header = "#chr\\tstart\\tstop\\t" + "\\t".join(samples)

                intersect_file = self.getIntersectFilename(
                    treatment=treatment,
                    target=target
                    )

                coverage_file = self.getCoverageFilename(
                    treatment=treatment,
                    target=target
                    )

                coverage_command = self.coverage_command.substitute(
                    header=header,
                    bamfiles=" ".join(bamfiles),
                    bedfile=intersect_file,
                    coverage_file=coverage_file,
                    num_treatments=len(bamfiles)//2
                    )
                coverage_commands_file.write(coverage_command + "\n")

        ### Cross-sample
        for treatment in self.treatments:
            for target in self.targets:
                # print("target: " + target + " treatment: " + treatment)

               ### Treated
                bamfiles = [self.getBamSample(
                    treatment=treatment,
                    target=target,
                    rep=rep,
                    )
                    for rep in self.samples["reps"]]
                ### Mock
                bamfiles += [self.getBamSample(
                    treatment=self.mockname,
                    target=target,
                    rep=rep,
                    )
                    for rep in self.samples["reps"]]

                ### Treatment
                samples = ["_".join([treatment, target, rep]) for rep in self.samples["reps"]]
                ### Mock
                samples += ["_".join([self.mockname, target, rep]) for rep in self.samples["reps"]]
                header = "#chr\\tstart\\tstop\\t" + "\\t".join(samples)

                ### treat vs mock
                treat_vs_mock_intersect = self.getIntersectFilename(
                    treatment=treatment + "_vs_" + self.mockname,
                    target=target
                    )
                treat_vs_mock_coverage = self.getCoverageFilename(
                    treatment=treatment + "_vs_" + self.mockname,
                    target=target
                    )
                coverage_command = self.coverage_command.substitute(
                    header=header,
                    bamfiles=" ".join(bamfiles),
                    bedfile=treat_vs_mock_intersect,
                    coverage_file=treat_vs_mock_coverage,
                    num_treatments=len(bamfiles)//2
                    )
                coverage_commands_file.write(coverage_command + "\n")

                ### mock vs treat
                mock_vs_treat_coverage = self.getCoverageFilename(
                    treatment=self.mockname + "_vs_" + treatment,
                    target=target
                    )
                mock_vs_treat_intersect = self.getIntersectFilename(
                    treatment=self.mockname + "_vs_" + treatment,
                    target=target
                    )
                coverage_command = self.coverage_command.substitute(
                    header=header,
                    bamfiles=" ".join(bamfiles),
                    bedfile=mock_vs_treat_intersect,
                    coverage_file=mock_vs_treat_coverage,
                    num_treatments=len(bamfiles)//2
                    )
                coverage_commands_file.write(coverage_command + "\n")

        coverage_commands_file.close()
    ### /writeCoverageCommands ###


    ### writeFoldChange ###
    def writeFoldChange(self ):
        ### This applies only to intersects
        ### Peak caller calculates fold changes
        peaksdir = self.getFullPath("peaks")
        coveragedir = self.getFullPath("coverage")

        for treatment in self.all_treatments:
            for target in self.targets:
                #print("target: " + target + " treatment: " + treatment)
                intersect_file = self.getIntersectFilename(
                    treatment=treatment,
                    target=target,
                    full_path=True
                    )

                #print("intersect_file: " + intersect_file)

                intersect_data = pd.read_csv(intersect_file, sep="\t")

                treatment_coverage_file = self.getCoverageFilename(
                    treatment=treatment,
                    target=target,
                    full_path=True
                    )
                treatment_coverage = pd.read_csv(treatment_coverage_file, sep="\t")
                #print("treatment_coverage_file: " + treatment_coverage_file)
                #print(treatment_coverage.head())

                input_coverage_file = self.getCoverageFilename(
                    treatment=treatment,
                    target=self.inputname,
                    full_path=True
                    )
                #print("input_coverage_file: " + input_coverage_file)
                input_coverage = pd.read_csv(input_coverage_file, sep="\t")
                #print(input_coverage.head())

                ### colums for chr# start stop
                intersect_coordinates = list(treatment_coverage.columns[0:3])
                ### columns for counts from each bam file
                treated = list(treatment_coverage.columns[3:])
                inputs = list(input_coverage.columns[3:])

                ### used for the total counts
                input_name = treatment + "_" + self.inputname
                treatment_name = treatment + "_" + target
                ### column names for individual counts
                input_samples = [input_name + "_" + rep for rep in self.samples["reps"]]
                treatment_samples = [treatment_name + "_" + rep for rep in self.samples["reps"]]
                #print("samples")
                #print(input_samples)
                #print(treatment_samples)

                ### can get the intersect coordinates from either treatment or input
                temp = input_coverage[intersect_coordinates]

                ### merge in input data and total counts from individual samples
                #print(input_samples + [input_name])
                temp = pd.merge(temp, input_coverage[input_samples], on=same)
                temp[input_name] =  input_coverage[input_samples].sum(axis=1)

                ### merge in treatment data and total counts from individual samples
                temp = pd.merge(temp, treatment_coverage[treatment_samples])
                temp[treatment_name] = treatment_coverage[treatment_samples].sum(axis=1)

                ### calculate fold change
                temp['fold'] = temp[treatment_name]/temp[sample_name]

                ### write file with fold change included
                fold_filename = "treatment" + "_" + "input" + "-intersect" + "-fold".bed
                temp.to_csv("", sqp="\t", quote='QUOTE_NONE')


    ### /writeFoldChange ###


    ### getFullPath ###
    def getFullPath(self, feature=""):
        if feature in self.directories:
            feature_data = self.directories[feature]
            full_path = feature_data['basedir'] + "/" + feature_data['local']
            # print("full path: " + full_path)
            return full_path
        else:
            return None
    ### /getFullPath ###


    ### getPeakSample ###
    def getPeakSample(self,
            treatment="",
            target="",
            rep="",
            full_path=True
            ):
        sample_string = treatment + "_" + target + "_" + rep + self.samples["peak_tag"]
        if full_path:
            sample_string = self.getFullPath("peaks") + "/" + sample_string
        # print("sample path: " + sample_string)

        return sample_string
    ### /getPeakSample ###


    ### getBamSample ###
    def getBamSample(self,
            treatment="",
            target="",
            rep="",
            full_path=True
            ):
        sample_string = treatment + "_" + target + "_" + rep + ".bam"
        if full_path:
            sample_string = self.getFullPath("bam") + "/" + sample_string

        # print("sample path: " + sample_string)

        return sample_string
    ### /getBamSample ###


    ### getIntersectFilename ###
    def getIntersectFilename(self,
            treatment="",
            target="",
            full_path=True
            ):

        sample_string = treatment + "_" + target \
                        + "-".join([""] + self.samples["reps"] + ["intersects"]) \
                        + ".bed"
        # print("coverage_name: " + coverage_name)
        if full_path:
            sample_string = self.getFullPath("intersects") + "/" + sample_string

        return sample_string
    ### /getIntersecttFilename ###

    ### getCoverageFilename ###
    def getCoverageFilename(self,
            treatment="",
            target="",
            full_path=True
            ):


        sample_string = treatment + "_" + target \
                        + "-".join([""] + self.samples["reps"] + ["coverage"]) \
                        + ".bed"
        # print("coverage_name: " + coverage_name)
        if full_path:
            sample_string = self.getFullPath("coverage") + "/" + sample_string

        return sample_string
    ### /getCoveragetFilename ###


    ### getCrossTreatmentPeakSample ###
    def getCrossTreatmentPeakSample(self,
            treatment="",
            target="",
            rep="",
            full_path=True
            ):

        treatment_vs_mock = \
            "_".join[treatment, "vs", self.samples["mockname"], rep] \
            + ".bed"
        mock_vs_treatment = \
            "_".join[i[""] + self.samples["mockname"], "vs", treatment, rep] \
            + ".bed"

        if full_path:
            treatment_vs_mock = self.getFullPath("peaks") \
                                + treatment_vs_mock
            mock_vs_treatment = self.getFullPath("peaks") \
                                + mock_vs_treatment

        # print("treatment_vs_mock: " + treatment_vs_mock)
        # print("mock_vs_treatment: " + mock_vs_treatment)

        return treatment_vs_mock, mock_vs_treatment
    ### /getIntersectFilename ###


if __name__ == "__main__":
    
    import argparse
    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="""Generate lists of commands for ChIP - Seq analysis.
            1) Create summary peak bed files of the form:

                chr	start	stop	input_cov	control_cov	log2_fold_change	log2_inverse_fold_change	q_value

            2) 
            3) Condor submit scripts""",
        )
    parser.add_argument('--config-file', '-cf',
        required=True,
        type=str,
        help="YAML configuration file"
        )
    args = parsier.parse_args()
    

