
# Python
import random
from collections import OrderedDict
from datetime import datetime

# PyFusion
from PyFusionGUI import *  # This contains the default file locations of import directories.
from pyfusion import DEFAULT_CONFIG_FILE

# Additional GUI Windows
from ClusteringWindow import *
from PinpointWindow import *
from ErrorWindow import *

# My Additions
from Utilities import jtools as jt
from Analysis import analysis
import backend
from CONSTANTS import *

# tkinter
try:  # Will work with python 3
    import tkinter as tk
    from tkinter.filedialog import askopenfilename, asksaveasfilename
    from tkinter.messagebox import showerror
except ImportError:  # Will work with python 2
    import Tkinter as tk
    from tkFileDialog import askopenfilename, asksaveasfilename
    from tkMessageBox import showerror, showinfo


class PyFusionWindow:
    def __init__(self):
        # Initializes a class of the PyFusionWindow. This method creates every label, entry, tkinterVar, etc.
        # needed for the window to be displayed. The varying secitons and frames are organized in order and
        # easily editable. In order to actually display the window, you must call PyFusionWindow.start()
        self.AN = None
        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.title("PyFusion GUI v. 0")
        #self.root.geometry("920x500")
        self.value_dict = OrderedDict()

        # ======================================
        # ======================================
        # ==         SHOT INFORMATION         ==
        # ======================================
        # ======================================
        self.col_0_frame = tk.Frame(master=self.root)
        self.col_0_frame.grid(row=0, column=0, sticky=tk.N)
        self.shot_frame = tk.Frame(master=self.col_0_frame, bd=5, relief=tk.SUNKEN)
        self.shot_frame.grid(padx=15, pady=15, row=0, column=0, sticky=tk.NW)
        self.shot_info = tk.Label(master=self.shot_frame,
                                  text="Shot Info",
                                  font=(font_name, 20))
        self.shot_info.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        self.shot_label = tk.Label(master=self.shot_frame,
                                   text="Shots:",
                                   font=font)
        self.shot_label.grid(row=1, sticky=tk.E)
        self.shot_help_label = tk.Label(master=self.shot_frame,
                                        text="Enter shot numbers and/or shot ranges separated" +
                                             "\nby commas. For example, 159243,159248-159255.",
                                        font=(font_name, 9))
        self.shot_help_label.grid(row=2, column=0, columnspan=2)
        self.shot_var = tk.StringVar(master=self.shot_frame)
        self.shots = tk.Entry(master=self.shot_frame,
                              font=font,
                              textvariable=self.shot_var)
        self.shots.grid(row=1, column=1, padx=5)

        self.time_label = tk.Label(master=self.shot_frame,
                                   text="Times:",
                                   font=font)
        self.time_label.grid(row=3, sticky=tk.E)
        self.time_help_label = tk.Label(master=self.shot_frame,
                                        text="Enter a time range in ms. For example, 300-1400.",
                                        font=(font_name, 9))
        self.time_help_label.grid(row=4, column=0, columnspan=2)
        self.time_var = tk.StringVar(master=self.shot_frame)
        self.times = tk.Entry(master=self.shot_frame,
                              font=font,
                              textvariable=self.time_var)
        self.times.grid(row=3, column=1, padx=5)

        self.probes_label = tk.Label(master=self.shot_frame,
                                     text="Probe Array:",
                                     font=font)
        self.probes_label.grid(row=5, sticky=tk.E)
        self.probes_help_label = tk.Label(master=self.shot_frame,
                                          text="Enter a probe array name. For example, DIIID_toroidal_mag." +
                                          "\nThese are defined in pyfusion.cfg",
                                          font=(font_name, 9))
        self.probes_help_label.grid(row=6, column=0, columnspan=2)
        self.probe_var = tk.StringVar(master=self.shot_frame)
        self.probes = tk.Entry(master=self.shot_frame,
                               font=font,
                               textvariable=self.probe_var)
        self.probes.grid(row=5, column=1, padx=5)

        self.clustering_label = tk.Label(master=self.shot_frame, text="\nClustering Variable", font=font)
        self.clustering_label.grid(row=7, column=0, columnspan=2, sticky=tk.N)
        self.clustering_var = tk.IntVar(master=self.shot_frame, value=0)
        self.clustering_but_phase = tk.Radiobutton(master=self.shot_frame, text="Use Phases\n(magnetic probes)",
                                                   variable=self.clustering_var, value=0)
        self.clustering_but_phase.grid(row=8, column=0, columnspan=2, sticky=tk.N)
        self.clustering_but_amp = tk.Radiobutton(master=self.shot_frame, text="Use Amplitudes\n(ECE probes)",
                                                 variable=self.clustering_var, value=1)
        self.clustering_but_amp.grid(row=9, column=0, columnspan=2, sticky=tk.N)
        # ======================================
        # ======================================
        # ==       DATAMINING SETTINGS        ==
        # ======================================
        # ======================================
        self.col_1_frame = tk.Frame(master=self.root)
        self.col_1_frame.grid(row=0, column=1, sticky=tk.N)
        self.dms_frame = tk.Frame(master=self.col_1_frame, bd=5, relief=tk.SUNKEN)
        self.dms_frame.grid(row=0, column=0)
        self.dms_info = tk.Label(master=self.dms_frame,
                                 text="Datamining Settings",
                                 font=(font_name, 20))
        self.dms_info.grid(row=0, column=0, columnspan=5, sticky=tk.N)
        self.ncpus_label = tk.Label(master=self.dms_frame,
                                    text="n_cpus:",
                                    font=font)
        self.ncpus_label.grid(row=1, column=0, sticky=tk.E)
        self.ncpus_help_label = tk.Label(master=self.dms_frame,
                                         text="Enter number of CPU's to use.",
                                         font=(font_name, 9))
        self.ncpus_help_label.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)
        self.ncpus_var = tk.StringVar(master=self.dms_frame)
        self.ncpus_entry = tk.Entry(master=self.dms_frame,
                                    width=9,
                                    font=font,
                                    textvariable=self.ncpus_var)
        self.ncpus_entry.grid(row=1, column=1, padx=5, sticky=tk.W)
        self.nclusters_label = tk.Label(master=self.dms_frame,
                                        text="n_clusters:",
                                        font=font)
        self.nclusters_label.grid(row=3, column=0, sticky=tk.E)
        self.nclusters_help_label = tk.Label(master=self.dms_frame,
                                             text="Enter number of clusters to look for.",
                                             font=(font_name, 9))
        self.nclusters_help_label.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW)
        self.nclusters_var = tk.StringVar(master=self.dms_frame)
        self.nclusters_entry = tk.Entry(master=self.dms_frame,
                                        width=9,
                                        font=font,
                                        textvariable=self.nclusters_var)
        self.nclusters_entry.grid(row=3, column=1, padx=5, sticky=tk.W)
        self.niter_label = tk.Label(master=self.dms_frame,
                                    text="n_iterations:",
                                    font=font)
        self.niter_label.grid(row=5, column=0, sticky=tk.E)
        self.niter_help_label = tk.Label(master=self.dms_frame,
                                         text="Enter number of clustering iterations.",
                                         font=(font_name, 9))
        self.niter_help_label.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW)
        self.niter_var = tk.StringVar(master=self.dms_frame)
        self.niter_entry = tk.Entry(master=self.dms_frame,
                                    font=font,
                                    width=9,
                                    textvariable=self.niter_var)
        self.niter_entry.grid(row=5, column=1, padx=5, sticky=tk.W)
        self.start_method_label = tk.Label(master=self.dms_frame,
                                           text="Start Method:",
                                           font=font)
        self.start_method_label.grid(row=7, column=0, sticky=tk.E)
        self.start_method_help_label = tk.Label(master=self.dms_frame,
                                                text="Enter starting clustering method.",
                                                font=(font_name, 9))
        self.start_method_help_label.grid(row=8, column=0, columnspan=2, sticky=tk.NSEW)
        self.start_method_var = tk.StringVar(master=self.dms_frame)
        self.start_method_entry = tk.Entry(master=self.dms_frame,
                                           font=font,
                                           width=9,
                                           textvariable=self.start_method_var)
        self.start_method_entry.grid(row=7, column=1, padx=5, sticky=tk.W)
        self.method_label = tk.Label(master=self.dms_frame,
                                     text="Method:",
                                     font=font)
        self.method_label.grid(row=9, column=0, sticky=tk.E)
        self.method_help_label = tk.Label(master=self.dms_frame,
                                          text="Enter final clustering method.",
                                          font=(font_name, 9))
        self.method_help_label.grid(row=10, column=0, columnspan=2, sticky=tk.NSEW)
        self.method_var = tk.StringVar(master=self.dms_frame)
        self.method_entry = tk.Entry(master=self.dms_frame,
                                     font=font,
                                     width=9,
                                     textvariable=self.method_var)
        self.method_entry.grid(row=9, column=1, padx=5, sticky=tk.W)
        self.freq_range_label = tk.Label(master=self.dms_frame,
                                         text="Freq. range:",
                                         font=font)
        self.freq_range_label.grid(row=11, column=0, sticky=tk.E)
        self.freq_range_help_label = tk.Label(master=self.dms_frame,
                                              text="Enter frequency range in kHz.\nFor example, 50-250.",
                                              font=(font_name, 9))
        self.freq_range_help_label.grid(row=12, column=0, columnspan=2, sticky=tk.NSEW)
        self.freq_range_var = tk.StringVar(master=self.dms_frame)
        self.freq_range_entry = tk.Entry(master=self.dms_frame,
                                         font=font,
                                         width=9,
                                         textvariable=self.freq_range_var)
        self.freq_range_entry.grid(row=11, column=1, padx=5, sticky=tk.W)

        self.seed_label = tk.Label(master=self.dms_frame,
                                   text="Seed:",
                                   font=font)
        self.seed_label.grid(row=1, column=3, sticky=tk.E)
        self.seed_help_label = tk.Label(master=self.dms_frame,
                                        text="Enter clustering seed.",
                                        font=(font_name, 9))
        self.seed_help_label.grid(row=2, column=3, columnspan=2, sticky=tk.NSEW)
        self.seed_var = tk.StringVar(master=self.dms_frame)
        self.seed_entry = tk.Entry(master=self.dms_frame,
                                   font=font,
                                   width=9,
                                   textvariable=self.seed_var)
        self.seed_entry.grid(row=1, column=4, padx=5, sticky=tk.W)
        self.random_seed_button = tk.Button(master=self.dms_frame,
                                            text="Random Seed",
                                            font=(font_name, 9),
                                            command=self.random_seed,
                                            bd=3)
        self.random_seed_button.grid(row=3, column=4, sticky=tk.NSEW)

        self.npeaks_label = tk.Label(master=self.dms_frame,
                                     text="n_peaks:",
                                     font=font).grid(row=5, column=3, sticky=tk.E)
        self.npeaks_help_label = tk.Label(master=self.dms_frame,
                                          text="Enter number of peaks to find.",
                                          font=(font_name, 9))
        self.npeaks_help_label.grid(row=6, column=3, columnspan=2, sticky=tk.NSEW)
        self.npeaks_var = tk.StringVar(master=self.dms_frame)
        self.npeaks_entry = tk.Entry(master=self.dms_frame,
                                     font=font,
                                     width=9,
                                     textvariable=self.npeaks_var)
        self.npeaks_entry.grid(row=5, column=4, padx=5, sticky=tk.W)

        self.cutoff_label = tk.Label(master=self.dms_frame,
                                     text="Cutoff By:",
                                     font=font)
        self.cutoff_label.grid(row=7, column=3, sticky=tk.E)
        self.cutoff_help_label = tk.Label(master=self.dms_frame,
                                          text="Enter cutoff by item.",
                                          font=(font_name, 9))
        self.cutoff_help_label.grid(row=8, column=3, columnspan=2, sticky=tk.NSEW)
        self.cutoff_var = tk.StringVar(master=self.dms_frame)
        self.cutoff_entry = tk.Entry(master=self.dms_frame,
                                     font=font,
                                     width=9,
                                     textvariable=self.cutoff_var)
        self.cutoff_entry.grid(row=7, column=4, padx=5, sticky=tk.W)
        self.cutoff_val_label = tk.Label(master=self.dms_frame,
                                         text="Cutoff Value:",
                                         font=font)
        self.cutoff_val_label.grid(row=9, column=3, sticky=tk.E)
        self.cutoff_val_help_label = tk.Label(master=self.dms_frame,
                                              text="Enter filter cutoff value.",
                                              font=(font_name, 9))
        self.cutoff_val_help_label.grid(row=10, column=3, columnspan=2, sticky=tk.NSEW)
        self.cutoff_val_var = tk.StringVar(master=self.dms_frame)
        self.cutoff_val_entry = tk.Entry(master=self.dms_frame,
                                         font=font,
                                         width=9,
                                         textvariable=self.cutoff_val_var)
        self.cutoff_val_entry.grid(row=9, column=4, padx=5, sticky=tk.W)
        self.filter_item_label = tk.Label(master=self.dms_frame,
                                          text="Filter Items:",
                                          font=font)
        self.filter_item_label.grid(row=11, column=3, sticky=tk.E)
        self.filter_item_help_label = tk.Label(master=self.dms_frame,
                                               text="Enter filter items.",
                                               font=(font_name, 9))
        self.filter_item_help_label.grid(row=12, column=3, columnspan=2, sticky=tk.NSEW)
        self.filter_item_var = tk.StringVar(master=self.dms_frame)
        self.filter_item_entry = tk.Entry(master=self.dms_frame,
                                          font=font,
                                          width=9,
                                          textvariable=self.filter_item_var)
        self.filter_item_entry.grid(row=11, column=4, padx=5, sticky=tk.W)


        # ======================================
        # ======================================
        # ==        SETTINGS BUTTONS          ==
        # ======================================
        # ======================================
        self.button_frame = tk.Frame(master=self.root)
        self.button_frame.grid(row=0, column=2, sticky=tk.N)
        self.settings_buttons_frame = tk.Frame(master=self.button_frame, bd=5, relief=tk.SUNKEN)
        self.settings_buttons_frame.grid(row=0, column=0, sticky=tk.N, padx=15, pady=15)

        self.settings_button_heading = tk.Label(master=self.settings_buttons_frame,
                                                text="Settings Options",
                                                font=font)
        self.settings_button_heading.grid(row=0, column=0, sticky=tk.N)
        self.save_settings_button = tk.Button(master=self.settings_buttons_frame,
                                              text="Save Settings",
                                              font=(font_name, 13), width=14,
                                              command=self.save_settings)
        self.save_settings_button.grid(row=1, column=0, sticky=tk.N)
        self.load_settings_button = tk.Button(master=self.settings_buttons_frame,
                                              text="Load From File",
                                              font=(font_name, 13), width=14,
                                              command=self.load_settings)
        self.load_settings_button.grid(row=2, column=0, sticky=tk.N)
        self.restore_defaults_button = tk.Button(master=self.settings_buttons_frame,
                                                 text="Restore Defaults",
                                                 font=(font_name, 13), width=14,
                                                 command=self.restore_defaults)
        self.restore_defaults_button.grid(row=3, column=0, sticky=tk.N)

        # ======================================
        # ======================================
        # ==        CLUSTERING BUTTONS        ==
        # ======================================
        # ======================================
        self.analysis_frame = tk.Frame(master=self.button_frame, bd=5, relief=tk.SUNKEN)
        self.analysis_frame.grid(row=1, column=0, sticky=tk.N, padx=15, pady=15)
        self.analysis_heading = tk.Label(master=self.analysis_frame,
                                         text="Analysis Options",
                                         font=font)
        self.analysis_heading.grid(row=0, column=0, sticky=tk.N)

        self.restore_clustering_button = tk.Button(master=self.analysis_frame,
                                                   text="Restore from\nPrevious Analysis",
                                                   font=(font_name, 13), width=14,
                                                   command=self.restore_clustering)
        self.restore_clustering_button.grid(row=1, column=0, sticky=tk.N)

        self.run_clustering_button = tk.Button(master=self.analysis_frame,
                                               text="Cluster from\nCurrent Settings",
                                               font=(font_name, 13), width=14,
                                               command=self.run_clustering)
        self.run_clustering_button.grid(row=2, column=0, sticky=tk.N)

        self.run_point_analysis_button = tk.Button(master=self.analysis_frame,
                                                   text="Pinpoint Analysis",
                                                   font=(font_name, 13), width=14,
                                                   command=self.run_point_analysis)
        self.run_point_analysis_button.grid(row=3, column=0, sticky=tk.N)
        self.run_point_analysis_help = tk.Label(master=self.analysis_frame,
                                                text="For plotting data at a certain"
                                                     "\ntime and frequency.",
                                                font=(font_name, 9))
        self.run_point_analysis_help.grid(row=4, column=0, sticky=tk.N)
        self.run_point_analysis_button.config(state="disabled")
        # ======================================
        # ======================================
        # ==         PLOTTING BUTTONS         ==
        # ======================================
        # ======================================

        def temp():
            # This function is used as a placeholder for the buttons below while the buttons are disabled.
            # Once the buttons are enabled, their commands will be reconfigured to the correct functions.
            return

        self.plotting_button_frame = tk.Frame(master=self.col_0_frame, bd=5, relief=tk.SUNKEN)
        self.plotting_button_frame.grid(row=2, column=0, sticky=tk.N)
        self.save_object_button = tk.Button(master=self.plotting_button_frame, text="Save Current\nAnalysis Object",
                                            font=(font_name, 13), width=14, command=temp)
        self.save_object_button.grid(row=0, column=0, sticky=tk.N)
        self.save_object_button.config(state="disabled")
        self.plot_clusters_button = tk.Button(master=self.plotting_button_frame, text="Plot\nClusters",
                                              font=(font_name, 13), width=14, command=temp)
        self.plot_clusters_button.grid(row=0, column=1, sticky=tk.N)
        self.plot_clusters_button.config(state="disabled")

        # ======================================
        # ======================================
        # ==          SLURM SETTINGS          ==
        # ======================================
        # ======================================
        self.slurm_frame = tk.Frame(master=self.col_1_frame, bd=5, relief=tk.SUNKEN)
        self.slurm_frame.grid(row=1, column=0, sticky=tk.N, pady=(0, 20))

        self.slurm_info = tk.Label(master=self.slurm_frame, text="SLURM Settings", font=(font_name, 20))
        self.slurm_info.grid(row=0, column=0, columnspan=2, sticky=tk.N)

        self.partition_label = tk.Label(master=self.slurm_frame, text="Partition:", font=font)
        self.partition_label.grid(row=1, column=0, sticky=tk.E)
        self.partition_var = tk.StringVar(master=self.slurm_frame, value="short")
        self.partition_entry = tk.Entry(master=self.slurm_frame, textvariable=self.partition_var, font=font)
        self.partition_entry.grid(row=1, column=1, sticky=tk.W)
        self.partition_help_label = tk.Label(master=self.slurm_frame,
                                             text="Enter short (20min), medium (1day), or long(1wk).", font=(font_name, 9))
        self.partition_help_label.grid(row=2, column=0, columnspan=2, sticky=tk.N)

        self.running_time_label = tk.Label(master=self.slurm_frame, text="Est. Run Time:", font=font)
        self.running_time_label.grid(row=3, column=0, sticky=tk.E)
        self.running_time_var = tk.StringVar(master=self.slurm_frame, value="")
        self.running_time_entry = tk.Entry(master=self.slurm_frame, textvariable=self.running_time_var, font=font)
        self.running_time_entry.grid(row=3, column=1, sticky=tk.W)
        self.running_time_help_label = tk.Label(master=self.slurm_frame,
                                                text="Enter in the upper bound for running time in minutes.\n"
                                                     "(Takes 1.5 minutes per shot average)", font=(font_name, 9))
        self.running_time_help_label.grid(row=4, column=0, columnspan=2, sticky=tk.N)

        self.mem_label = tk.Label(master=self.slurm_frame, text="Max Memory Usage:", font=font)
        self.mem_label.grid(row=5, column=0, sticky=tk.E)
        self.mem_var = tk.StringVar(master=self.slurm_frame, value="115G")
        self.mem_entry = tk.Entry(master=self.slurm_frame, textvariable=self.mem_var, font=font)
        self.mem_entry.grid(row=5, column=1, sticky=tk.W)
        self.mem_help = tk.Label(master=self.slurm_frame, text="Enter in the maximum amount of memory and units.\n"
                                                               "Recommended: 115G. Units: M (Mb) or G (Gb)")
        self.mem_help.grid(row=6, column=0, columnspan=2, sticky=tk.N)

        # ======================================
        # ======================================
        # ==          MISC. WIDGETS           ==
        # ======================================
        # ======================================
        self.misc_frame = tk.Frame(master=self.button_frame, bd=5, relief=tk.SUNKEN)
        self.misc_frame.grid(row=2, column=0, sticky=tk.N)
        self.misc_heading = tk.Label(master=self.misc_frame,
                                     text="Other Options",
                                     font=font)
        self.misc_heading.grid(row=0, column=0, sticky=tk.N)
        self.close_button = tk.Button(master=self.misc_frame,
                                      text="Close Window",
                                      font=(font_name, 13), width=14,
                                      command=self.root.destroy)
        self.close_button.grid(row=1, column=0, sticky=tk.N)

        self.using_analysis_var = tk.StringVar(master=self.col_0_frame, value="No analysis object loaded yet.\n"
                                               "Please perform clustering or\nrestore an anlysis object.")
        self.using_analysis_label = tk.Label(master=self.col_0_frame,
                                             textvariable=self.using_analysis_var,
                                             font=(font_name, 14, "bold"), fg="red")
        self.using_analysis_label.grid(row=1, column=0, sticky=tk.N)

        # ====================================== #
        # ====================================== #
        # ==             BINDINGS             == #
        # ====================================== #
        # ====================================== #
        self.root.bind("<<clustering_restored>>", self.clustering_restored)
        self.root.bind("<<slurm_clustering_complete>>", self.slurm_clustering_complete)
        self.root.bind("<<clustering_in_progress>>", self.clustering_in_progress)
        self.root.bind("<<clustering_failed>>", self.clustering_failed)

        # ====================================== #
        # ====================================== #
        # ==      SAVING INITIAL VALUES       == #
        # ====================================== #
        # ====================================== #
        self.value_dict["shots"] = self.shot_var
        self.value_dict["times"] = self.time_var
        self.value_dict["probe_array"] = self.probe_var
        self.value_dict["n_cpus"] = self.ncpus_var
        self.value_dict["n_clusters"] = self.nclusters_var
        self.value_dict["n_iterations"] = self.niter_var
        self.value_dict["start"] = self.start_method_var
        self.value_dict["method"] = self.method_var
        self.value_dict["freq_range"] = self.freq_range_var
        self.value_dict["seed"] = self.seed_var
        self.value_dict["n_peaks"] = self.npeaks_var
        self.value_dict["cutoff_by"] = self.cutoff_var
        self.value_dict["cutoff_value"] = self.cutoff_val_var
        self.value_dict["filter_items"] = self.filter_item_var
        self.value_dict["partition"] = self.partition_var
        self.value_dict["run_time"] = self.running_time_var
        self.value_dict["mem"] = self.mem_var
        self.value_dict["clustering_variable"] = self.clustering_var
        return

    def start(self):
        # This method begins the window's mainloop and displays it
        self.restore_defaults()
        self.root.mainloop()
        return None

    def load_settings(self):
        # A window will pop up asking the user to specify a file containing the default values for
        # the PyFusionWindow entries.
        fname = askopenfilename(initialdir=GUI_DIR,
                                filetypes=(("GUI Config File", "*.guiconfig"), ("All Files", "*.*")))
        if fname == "" or fname == (): return None
        try: self.load_values_from_file(fname)
        except: ErrorWindow(self.root, "Incorrect file format.")
        return None

    def save_settings(self):
        # A window will pop up asking the user where they would like to save the current GUI settings.
        if self.valid_values():
            fname = asksaveasfilename(initialdir=GUI_DIR,
                                      filetypes=(("GUI Config File", "*.guiconfig"), ("All Files", "*.*")))
            if fname == "" or fname == (): return None
            backend.save_values(self.value_dict, fname)
            return None

    def defaults_missing(self):
            # This method will be called in the event that the default .guiconfig file cannot be found. Some
            # default values are hard coded below.
        defaults = '''shots: 159243
times: 300-1400
probe_array: DIIID_toroidal_mag
n_cpus: 1
n_clusters: 16
n_iterations: 20
start: k_means
method: EM_VMM
freq_range: 50-250
seed: 743
n_peaks: 20
cutoff_by: sigma_eq
cutoff_value: 80
filter_items: EM_VMM_kappas
partition: short
run_time: 15
mem: 115G'''
        self.load_values_from_str(defaults)
        with open(os.path.join(GUI_DIR, ".guiconfig"), "w") as new_default:
            new_default.write(defaults)
        return

    def restore_defaults(self):
        # This method will try to load the default settings from the DEFAULT_SETTINGS_DIR in CONSTANTS.py.
        # If there is an error (file not found or corrupted file), it will call PyFusionWindow.defaults_missing().
        try:
            self.load_values_from_file(DEFAULT_SETTINGS_DIR)
        except:
            self.defaults_missing()
        return None

    def load_values_from_str(self, s):
        # Loads in GUI config values from a string, s. This method does NOT check for the integrity of the
        # values or if they are valid.
        lines = s.split("\n")
        for line in lines:
            val = line.split(":")[1].strip()
            if line.startswith("shots"): self.shot_var.set(val)
            elif line.startswith("times"): self.time_var.set(val)
            elif line.startswith("probe_array"): self.probe_var.set(val)
            elif line.startswith("n_cpus"): self.ncpus_var.set(val)
            elif line.startswith("n_clusters"): self.nclusters_var.set(val)
            elif line.startswith("n_iterations"): self.niter_var.set(val)
            elif line.startswith("start"): self.start_method_var.set(val)
            elif line.startswith("method"): self.method_var.set(val)
            elif line.startswith("freq_range"): self.freq_range_var.set(val)
            elif line.startswith("seed"): self.seed_var.set(val)
            elif line.startswith("n_peaks"): self.npeaks_var.set(val)
            elif line.startswith("cutoff_by"): self.cutoff_var.set(val)
            elif line.startswith("cutoff_value"): self.cutoff_val_var.set(val)
            elif line.startswith("filter_item"): self.filter_item_var.set(val)
            elif line.startswith("partition"): self.partition_var.set(val)
            elif line.startswith("mem"): self.mem_var.set(val)
            elif line.startswith("run_time"): self.running_time_var.set(val)
        return

    def load_values_from_file(self, f):
        # Opens a file containing GUI config values and attemps to parse them with
        # PyFusionWindow.load_values_from_str().
        with open(f) as vals:
            settings = vals.read()
        self.load_values_from_str(settings)
        return

    def valid_values(self):
        # Goes through each parameter and checks its validity using routines from jtools.py. If a parameter
        # is not valid, an ErrorWindow will open up displaying the offending variable.
        valid = True
        if not jt.valid_shot_str(self.value_dict["shots"].get()):
            ErrorWindow(self.root, "Shots entry is invalid.")
            valid = False
        if not jt.valid_window(self.value_dict["times"].get()):
            ErrorWindow(self.root, "Time window entry is invalid.")
            valid = False
        if not jt.valid_probe_array(self.value_dict["probe_array"].get()):
            ErrorWindow(self.root, "Probe array is not valid! Please enter a valid" +
                        " probe array name from:\n{}".format(jt.scan_config(DEFAULT_CONFIG_FILE)))
            valid = False
        if not jt.valid_int_from_str(self.value_dict["n_cpus"].get()):
            ErrorWindow(self.root, "Number of CPUs must be an integer.")
            valid = False
        if not jt.valid_int_from_str(self.value_dict["n_clusters"].get()):
            ErrorWindow(self.root, "Number of clusters must be an integer.")
            valid = False
        if not jt.valid_int_from_str(self.value_dict["n_iterations"].get()):
            ErrorWindow(self.root, "Number of iterations must be an integer.")
            valid = False
        if not jt.valid_method(self.value_dict["method"].get()):
            ErrorWindow(self.root, "Method must be in: {}. To add a new method to this list," +
                        " edit ""return_methods()"" in Utilities/jtools.py")
            valid = False
        if not jt.valid_window(self.value_dict["freq_range"].get()):
            ErrorWindow(self.root, "Frequency range entry is invalid.")
            valid = False
        if not jt.valid_int_from_str(self.value_dict["seed"].get()):
            ErrorWindow(self.root, "Seed must be an integer.")
            valid = False
        if not jt.valid_int_from_str(self.value_dict["n_peaks"].get()):
            ErrorWindow(self.root, "Number of peaks must be an integer.")
            valid = False
        # Not sure how to test cutoff_by...
        if not jt.valid_int_from_str(self.value_dict["cutoff_value"].get()):
            ErrorWindow(self.root, "Cutoff value must be an integer.")
            valid = False
        # Not sure how to test filter_items... :(
        # Checks the contents of "every" cell to ensure the contents are valid.
        if self.value_dict["partition"].get().lower().strip() not in ["short", "medium", "long"]:
            ErrorWindow(self.root, "Partition must be short, medium, or long.")
            valid = False
        if not jt.valid_float_from_str(self.value_dict["run_time"].get()) or \
                        float(self.value_dict["run_time"].get()) > 19:
            ErrorWindow(self.root, "Estimated run time must be a float or integer!")
            valid = False
        if not jt.valid_float_from_str(self.value_dict["mem"].get()[:-1]) or \
                        self.value_dict["mem"].get()[-1].lower().strip() not in ["g", "m"]:
            ErrorWindow(self.root, "Max memory usage entry is not valid.")
            valid = False
        return valid

    def random_seed(self):
        # Generates a random clustering seed between 1 and 10,000 and saves it to PyFusionWindow.seed_var
        # as a tkinter IntVar.
        self.seed_var.set(str(random.choice(range(1, 10001))))
        return None

    def settings_to_datamining_object_str(self):
        # Parses current GUI settings  into variables used to create a DataMining object.
        # This method only returns a string which, when executed in the proper environment,
        # will generate a DataMining object.
        shots = jt.shot_str_parser(self.value_dict["shots"].get())
        time_windows = jt.time_window_parser(self.value_dict["times"].get())
        probes = self.value_dict["probe_array"].get()
        n_cpus = int(self.value_dict["n_cpus"].get())
        n_clusters = int(self.value_dict["n_clusters"].get())
        n_iterations = int(self.value_dict["n_iterations"].get())
        start = self.value_dict["start"].get()
        method = self.value_dict["method"].get()
        freq_range = jt.time_window_parser(self.value_dict["freq_range"].get())
        lower_freq = freq_range[0]
        upper_freq = freq_range[1]
        seeds = int(self.value_dict["seed"].get())
        n_peaks = int(self.value_dict["n_peaks"].get())
        cutoff_by = self.value_dict["cutoff_by"].get()
        cutoff_value = int(self.value_dict["cutoff_value"].get())
        filter_items = self.value_dict["filter_items"].get()
        if self.clustering_var.get() == 0:
            use_amp = False
        elif self.clustering_var.get() == 1:
            use_amp = True
        else:
            use_amp = None
        datamining_settings = {'n_clusters': n_clusters, 'n_iterations': n_iterations,
                               'start': start, 'verbose': 0, 'method': method, "seeds": seeds,
                               "amplitude": use_amp}
        fft_settings = {"n_pts": n_peaks, "lower_freq": lower_freq, "upper_freq": upper_freq,
                        "cutoff_by": cutoff_by, "ave_kappa_cutoff": cutoff_value, "filter_item": filter_items}
        return "DataMining(shots={shots}, time_windows={time_windows}, probes=\"{probes}\","\
               "datamining_settings={datamining_settings}, fft_settings={fft_settings},"\
               "n_cpus={n_cpus})".format(shots=shots, time_windows=time_windows, probes=probes,
                                         datamining_settings=datamining_settings,
                                         fft_settings=fft_settings, n_cpus=n_cpus)


    @staticmethod
    def datamining_str_to_analysis_object_str(DM):
        # Given a DataMining object string from PyFusionWindow.settings_to_datamining_object_str(), will
        # return a string of the constructor to create an Analysis object.
        return "Analysis(DM={})".format(DM)

    def settings_to_analysis_object_str(self):
        # Checks the validity of the current GUI config settings and returns a string of the constructor
        # of an Analysis object.
        if self.valid_values():
            DMstr = self.settings_to_datamining_object_str()
            return self.datamining_str_to_analysis_object_str(DMstr)

    def save_analysis_object(self):
        fname = askopenfilename(initialdir=IRIS_CSCRATCH_DIR,
                                filetypes=(("Analysis File Object", "*.ANobj"), ("All Files", "*.*")))
        if fname == "" or fname == (): return None
        try:
            self.AN.save(fname)
        except:
            ErrorWindow(master=self.root, message="Unable to save file due to unknown error.")
        return

    def restore_clustering(self):
        # A window pops up asking the user to specify the path of a *.ANobj (Analysis Object) file
        # and attempts to restore it using the Analysis.restore classmethod. Then opens a ClusteringWindow
        # which gives the user the option to plot clusters, save the object, or close the window.
        fname = askopenfilename(initialdir=IRIS_CSCRATCH_DIR,
                                filetypes=(("Analysis File Object", "*.ANobj"), ("All Files", "*.*")))
        if fname == "" or fname == (): return None
        try:
            self.AN = analysis.Analysis.restore(fname)
            self._restore_settings_from_loaded_object()
            self.root.event_generate("<<clustering_restored>>", when="tail")
            self.using_analysis_var.set("Using analysis object from\n{}".format(jt.break_path(fname, 24)))
            self.using_analysis_label.config(fg="dark green")
        except:
            ErrorWindow(self.root, "Incorrect file format.")
        return None

    def return_restored_object_values(self):
        # Returns a dictionary containing all of the settings used to create the currently
        # loaded Analysis Object.
        return {"shots": jt.reverse_shot_str_parser(self.AN.DM.shot_info["shots"]),
                "times": jt.ANobj_times_to_time_window(self.AN.DM.shot_info["time_windows"]),
                "probe_array": self.AN.DM.shot_info["probes"],
                "n_cpus": str(self.AN.DM.n_cpus),
                "n_clusters": str(self.AN.DM.datamining_settings["n_clusters"]),
                "n_iterations": str(self.AN.DM.datamining_settings["n_iterations"]),
                "start": self.AN.DM.datamining_settings["start"],
                "method": self.AN.DM.datamining_settings["method"],
                "freq_range": str(self.AN.DM.fft_settings["lower_freq"]) + "-" +
                              str(self.AN.DM.fft_settings["upper_freq"]),
                "seed": str(self.AN.DM.datamining_settings["seeds"]),
                "n_peaks": str(self.AN.DM.fft_settings["n_pts"]),
                "cutoff_by": self.AN.DM.fft_settings["cutoff_by"],
                "cutoff_value": str(self.AN.DM.fft_settings["ave_kappa_cutoff"]),
                "filter_items": self.AN.DM.fft_settings["filter_item"]}

    def _restore_settings_from_loaded_object(self):
        # Loads the settings used to analyze an Analysis object that has been loaded.
        self.value_dict["shots"].set(jt.reverse_shot_str_parser(self.AN.DM.shot_info["shots"]))
        self.value_dict["times"].set(jt.ANobj_times_to_time_window(self.AN.DM.shot_info["time_windows"]))
        self.value_dict["probe_array"].set(self.AN.DM.shot_info["probes"])
        self.value_dict["n_cpus"].set(str(self.AN.DM.n_cpus))
        self.value_dict["n_clusters"].set(str(self.AN.DM.datamining_settings["n_clusters"]))
        self.value_dict["n_iterations"].set(str(self.AN.DM.datamining_settings["n_iterations"]))
        self.value_dict["start"].set(self.AN.DM.datamining_settings["start"])
        self.value_dict["method"].set(self.AN.DM.datamining_settings["method"])
        self.value_dict["freq_range"].set(str(self.AN.DM.fft_settings["lower_freq"])+"-"+
                                          str(self.AN.DM.fft_settings["upper_freq"]))
        self.value_dict["seed"].set(str(self.AN.DM.datamining_settings["seeds"]))
        self.value_dict["n_peaks"].set(str(self.AN.DM.fft_settings["n_pts"]))
        self.value_dict["cutoff_by"].set(self.AN.DM.fft_settings["cutoff_by"])
        self.value_dict["cutoff_value"].set(str(self.AN.DM.fft_settings["ave_kappa_cutoff"]))
        self.value_dict["filter_items"].set(self.AN.DM.fft_settings["filter_item"])
        self.value_dict["clustering_variable"].set(self.AN.DM.datamining_settings["amplitude"])
        return

    def clustering_restored(self, e):
        # This method is called when the root window receives the <<clustering_restored>> event
        # and opens a window  allowing the user to plot clusters, save the analysis object or close.
        self.plot_clusters_button.config(state="normal", command=self.AN.show_plots)
        self.save_object_button.config(state="normal", command=self.save_analysis_object)
        self.run_point_analysis_button.config(state="normal")
        return

    def run_clustering(self):
        # In order to run the clustering, we need to create a python script which does the analysis and saving
        # and also a SLURM sbatch script which we will use to submit a job to the high CPU-power worker nodes
        # on IRIS.
        # TODO: Allow the user to specify the #SBATCH settings within the GUI
        self.AN = None
        self.plot_clusters_button.config(state="disabled")
        self.save_object_button.config(state="disabled")
        if self.valid_values():
            now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            self.AN = IRIS_CSCRATCH_DIR + now + ".ANobj"

            pythonscript = '''from PyFusionGUI.Analysis.analysis import *
A1 = {ANALYSIS_OBJECT}
A1.save(\"{ANOBJ_FILE}\")
'''.format(ANALYSIS_OBJECT=self.settings_to_analysis_object_str(),
           ANOBJ_FILE=self.AN)

            with open(os.path.join(SLURM_DIR, "temp.py"), "w") as test:
                test.write(pythonscript)

            sbatchscript = '''#!/bin/bash
#SBATCH -p {PARTITION}
#SBATCH -n {N_CPUS}
#SBATCH -N 1
#SBATCH -t {RUN_TIME}
#SBATCH --mem {MEM}
#SBATCH -o /home/%u/PyFusionGUI/PyFusionGUI/SLURM/PyFusionGUI-%j.out
#SBATCH --export=ALL
set -e
echo "Starting job on worker node"
/fusion/usc/opt/python/2.7.11/bin/python2.7 {SCRIPT}
'''.format(PARTITION=self.value_dict["partition"].get(),
           N_CPUS=self.value_dict["n_cpus"].get(),
           RUN_TIME=self.value_dict["run_time"].get(),
           MEM=self.value_dict["mem"].get(),
           SCRIPT=os.path.join(SLURM_DIR, "temp.py"))

            with open(os.path.join(SLURM_DIR, "sbatch_clustering.sbatch"), "w") as sbatch:
                sbatch.write(sbatchscript)
            slurm_output = subprocess.check_output(
                "sbatch {}".format(os.path.join(SLURM_DIR, "sbatch_clustering.sbatch")), shell=True)
            jobid = jt.slurm_id_from_output(slurm_output)
            self.root.event_generate("<<clustering_in_progress>>", when="tail")
            win = ClusteringWindow(master=self.root, slurm_start_time=now, jobid=jobid)
            win.start()
            #self.root.after(10000, self.check_and_load_analysis_object, jobid, IRIS_CSCRATCH_DIR + now + ".ANobj")
            return

    def check_and_load_analysis_object(self, jobid, ANobj_file):
        # Checks SLURM to see if the analysis is done yet, and if it is, it will load it into
        # working memory.
        sjobexitmod_output = subprocess.check_output("sjobexitmod -l {}".format(jobid), shell=True)
        exit_state = jt.get_slurm_exit_state(sjobexitmod_output)
        if exit_state == "PENDING" or exit_state == "assigned" or exit_state == "RUNNING":
            pass
        elif exit_state == "COMPLETED":
            try:
                self.AN = analysis.Analysis.restore(ANobj_file)
                self.using_analysis_var.set("Clustering restored from\ncurrent settings using the\n"
                                            "worker node.")
                self.using_analysis_label.config(fg="dark green")
                self.root.event_generate("<<clustering_restored>>", when="tail")
            except:
                ErrorWindow(master=self.root, message="Unable to load recent Analysis object!\n"
                                                      "File is corrupted or out of memory.")
            return
        elif exit_state == "FAILED" or exit_state == "CANCELLED+":
            self.root.event_generate("<<clustering_failed>>", when="tail")
            return
        self.root.after(5000, self.check_and_load_analysis_object, jobid, ANobj_file)
        return

    def clustering_in_progress(self, e):
        # Changes the status message and color.
        self.using_analysis_var.set("Now clustering. Please wait.")
        self.using_analysis_label.config(fg="DarkOrange1")

    def slurm_clustering_complete(self, e):
        # Changes the status message and color, and loads the Analysis object. Whenever this method is called,
        # self.AN \\\SHOULD\\\ be a string of the file path to the recently clustered analysis object.
        self.using_analysis_var.set("Clustering on worker node\ncomplete. Analysis object loaded.")
        self.using_analysis_label.config(fg="dark green")
        self.AN = analysis.Analysis.restore(filename=self.AN)
        self.root.event_generate("<<clustering_restored>>", when="tail")
        self.run_point_analysis_button.config(state="normal")
        return

    def clustering_failed(self, e):
        # Changes the status message and color.
        self.using_analysis_var.set("Clustering Failed. No analysis object\n"
                                    "loaded yet. Please perform clustering\n"
                                    "or restore a saved analysis object")
        self.using_analysis_label.config(fg="red")
        return

    def run_point_analysis(self):
        # A window needs to popup asking the user for a frequency and time.
        # Verify both frequency and time are within our analysis windows.
        # Can only be done after the analysis has been performed. (Grey out button before that??)
        # but we'll ignore the latter for now.
        def valid_values():
            valid = True
            if not jt.valid_int_from_str(shot_var.get()):
                ErrorWindow(root, "Shot entry is invalid.")
                valid = False
            if not jt.valid_window(time_window_var.get()):
                ErrorWindow(root, "Time window entry is invalid.")
                valid = False
            if not jt.valid_window(freq_range_var.get()):
                ErrorWindow(root, "Frequency range entry is invalid.")
                valid = False
            if not jt.valid_float_from_str(time_var.get()) or not jt.t_in_window(time_var.get(), time_window_var.get()):
                ErrorWindow(root, "Time entry is invalid.")
                valid = False
            if not jt.valid_float_from_str(freq_var.get()) or not jt.t_in_window(freq_var.get(), freq_range_var.get()):
                ErrorWindow(root, "Frequency entry is invalid.")
                valid = False
            return valid

        def verify_cancel():
            win = tk.Toplevel(master=root)
            win.resizable(width=False, height=False)
            win.grab_set()
            label = tk.Label(master=win, text="Do you really wish\nto close?", font=(font_name, 18))
            label.grid(row=0, column=0, columnspan=2, sticky=tk.N)
            yes = tk.Button(master=win, text="Yes", font=(font_name, 18), command=root.destroy)
            yes.grid(row=1, column=0, sticky=tk.N)
            no = tk.Button(master=win, text="No", font=(font_name, 18), command=win.destroy)
            no.grid(row=1, column=1, sticky=tk.N)
            return

        def cont():
            if not valid_values():
                return
            fig, \
            ax1,  \
            ax2,   \
            ax3 = self.AN.return_pinpoint_plots(shot=shot_var.get(),
                                                t0=float(time_var.get()), f0=float(freq_var.get()),
                                                time_window=jt.time_window_parser(time_window_var.get()),
                                               frequency_window=jt.time_window_parser(freq_range_var.get()),
                                                clusters="all")
            plt.show()
            return


        root = tk.Toplevel(master=self.root)
        root.wm_protocol("WM_DELETE_WINDOW", verify_cancel)
        root.resizable(width=False, height=False)
        heading_label = tk.Label(master=root, text="Pinpoint Analysis", font=(font_name, 24))
        heading_label.grid(row=0, column=0, columnspan=2, sticky=tk.N)
        shot_label = tk.Label(master=root, text="Shot:", font=font)
        shot_label.grid(row=1, column=0, sticky=tk.NE)
        shot_var = tk.StringVar(master=root)
        shot_entry = tk.Entry(master=root, font=font, textvariable=shot_var)
        shot_entry.grid(row=1, column=1, sticky=tk.N)
        shot_help_label = tk.Label(master=root, text="Enter shot number", font=(font_name, 9))
        shot_help_label.grid(row=2, column=0, columnspan=2, sticky=tk.N)
        time_window_label = tk.Label(master=root, text="Time Window (ms):", font=font)
        time_window_label.grid(row=3, column=0, sticky=tk.NE)
        time_window_var = tk.StringVar(master=root)
        time_window_entry = tk.Entry(master=root, font=font, textvariable=time_window_var)
        time_window_entry.grid(row=3, column=1, sticky=tk.N)
        time_window_help_label = tk.Label(master=root,
                                          text="Enter time window (plotting purposes only). e.g. 300-500",
                                          font=(font_name, 9))
        time_window_help_label.grid(row=4, column=0, columnspan=2, sticky=tk.N)
        freq_range_label = tk.Label(master=root, text="Freq. Range (kHz):", font=font)
        freq_range_label.grid(row=5, column=0, sticky=tk.NE)
        freq_range_var = tk.StringVar(master=root)
        freq_range_entry = tk.Entry(master=root, font=font, textvariable=freq_range_var)
        freq_range_entry.grid(row=5, column=1, sticky=tk.N)
        freq_range_help_label = tk.Label(master=root,
                                         text="Enter frequency range (plotting purposes only). e.g. 50-250",
                                         font=(font_name, 9))
        freq_range_help_label.grid(row=6, column=0, columnspan=2, sticky=tk.N)
        time_label = tk.Label(master=root, text="Time (ms):", font=font)
        time_label.grid(row=7, column=0, sticky=tk.NE)
        time_var = tk.StringVar(master=root)
        time_entry = tk.Entry(master=root, font=font, textvariable=time_var)
        time_entry.grid(row=7, column=1, sticky=tk.N)
        time_help_label = tk.Label(master=root,
                                   text="Enter the time you would like to pinpoint. e.g. 534.23",
                                   font=(font_name, 9))
        time_help_label.grid(row=8, column=0, columnspan=2, sticky=tk.N)
        freq_label = tk.Label(master=root, text="Freq. (kHz):", font=font)
        freq_label.grid(row=9, column=0, sticky=tk.NE)
        freq_var = tk.StringVar(master=root)
        freq_entry = tk.Entry(master=root, font=font, textvariable=freq_var)
        freq_entry.grid(row=9, column=1, sticky=tk.N)
        freq_help_label = tk.Label(master=root,
                                   text="Enter the freq you would like to pinpoint. e.g. 63.42",
                                   font=(font_name, 9))
        freq_help_label.grid(row=10, column=0, columnspan=2, sticky=tk.N)
        button_frame = tk.Frame(master=root, bd=5, relief=tk.SUNKEN)
        button_frame.grid(row=11, column=1, sticky=tk.E)
        continue_button = tk.Button(master=button_frame, text="Continue", font=font, command=cont)
        continue_button.grid(row=0, column=0, sticky=tk.E)
        cancel_button = tk.Button(master=button_frame, text="Cancel", font=font, command=verify_cancel)
        cancel_button.grid(row=0, column=1, sticky=tk.W)
        root.grab_set()
        defaults = [str(jt.shot_str_parser(self.value_dict["shots"].get())[0]),
                    self.value_dict["times"].get(),
                    self.value_dict["freq_range"].get()]
        shot_var.set(defaults[0])
        time_window_var.set(defaults[1])
        freq_range_var.set(defaults[2])
        # if self.AN is None:
        #     if self.valid_values():
        #         defaults = [str(jt.shot_str_parser(self.value_dict["shots"].get())[0]),
        #                     self.value_dict["times"].get(),
        #                     self.value_dict["freq_range"].get()]
        #     else:
        #         return
        # else:
        #     object_settings = self.return_restored_object_values()
        #     defaults = [object_settings["shots"].split(",")[0], object_settings["times"],
        #                 object_settings["freq_range"]]
        # PinpointWindow(master=self.root, defaults=defaults, pf_window=self, previous_analysis=self.AN)
        return

if __name__ == "__main__":
    win = PyFusionWindow()
    win.start()