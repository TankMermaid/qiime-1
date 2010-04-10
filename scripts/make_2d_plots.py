#!/usr/bin/env python
# File created on 09 Feb 2010
#file make_2d_plots.py

from __future__ import division

__author__ = "Jesse Stombaugh"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Jesse Stombaugh"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Jesse Stombaugh"
__email__ = "jesse.stombaugh@colorado.edu"
__status__ = "Development"
 
 
from matplotlib import use
use('Agg',warn=False)
import matplotlib,re
from qiime.util import parse_command_line_parameters, get_options_lookup
from optparse import make_option
from qiime.make_2d_plots import generate_2d_plots
from qiime.parse import parse_coords,group_by_field,group_by_fields
import shutil
import os
from qiime.colors import sample_color_prefs_and_map_data_from_options
from qiime.util import get_qiime_project_dir
from qiime.make_3d_plots import get_coord
from cogent.util.misc import get_random_directory_name

options_lookup = get_options_lookup()

#make_2d_plots.py
script_info={}
script_info['brief_description']="""Make 2D PCoA Plots"""
script_info['script_description']="""This script generates 2D PCoA plots using the principal coordinates file generated by performing beta diversity measures of an OTU table."""
script_info['script_usage']=[]
script_info['script_usage'].append(("""Default Example:""","""If you just want to use the default output, you can supply the principal coordinates file (i.e., resulting file from principal_coordinates.py), where the default coloring will be based on the SampleID as follows:""","""%prog -i beta_div_coords.txt"""))
script_info['script_usage'].append(("""Output Directory Usage:""","""If you want to give an specific output directory (e.g. \"2d_plots\"), use the following code.""", """%prog -i beta_div_coords.txt -o 2d_plots/"""))
script_info['script_usage'].append(("""Mapping File Usage:""","""Additionally, the user can supply their mapping file ("-m") and a specific category to color by ("-b") or any combination of categories. When using the -b option, the user can specify the coloring for multiple mapping labels, where each mapping label is separated by a comma, for example: -b \'mapping_column1,mapping_column2\'. The user can also combine mapping labels and color by the combined label that is created by inserting an \'&&\' between the input columns, for example: -b \'mapping_column1&&mapping_column2\'.

If the user wants to color by specific mapping labels, they can use the following code:""","""%prog -i beta_div_coords.txt -m Mapping_file.txt -b 'mapping_column'"""))
script_info['script_usage'].append(("""""","""If the user would like to color all categories in their metadata mapping file, they can pass 'ALL' to the '-b' option, as follows:""","""%prog -i beta_div_coords.txt -m Mapping_file.txt -b ALL"""))
script_info['script_usage'].append(("""Output Directory Usage:""","""If you want to give an specific output directory (e.g. \"2d_plots\"), use the following code.""", """%prog -i beta_div_coords.txt -o 2d_plots/"""))
script_info['script_usage'].append(("""Combination of Features:""","""or use some of the suggestions from above:""", """%prog -i beta_div_coords.txt -m Mapping_file.txt -b \'mapping_column1,mapping_column1&&mapping_column2\'"""))
script_info['output_description']="""This script generates an output folder, which contains several files. To best view the 2D plots, it is recommended that the user views the _pca_2D.html file."""

script_info['required_options']=[\
make_option('-i', '--coord_fname', dest='coord_fname', \
help='This is the path to the principal coordinates file (i.e., resulting \
file from principal_coordinates.py)'),
make_option('-m', '--map_fname', dest='map_fname', \
     help='This is the metadata mapping file [default=%default]')
]
script_info['optional_options']=[\
make_option('-b', '--colorby', dest='colorby',\
     help='This is the categories to color by in the plots from the \
user-generated mapping file. The categories must match the name of a column \
header in the mapping file exactly and multiple categories can be list by comma \
separating them without spaces. The user can also combine columns in the \
mapping file by separating the categories by "&&" without spaces \
[default=%default]'),
 make_option('-p', '--prefs_path',help='This is the user-generated preferences \
file. NOTE: This is a file with a dictionary containing preferences for the \
analysis [default: %default]'),
 make_option('-k', '--background_color',help='This is the background color to \
use in the plots. [default: %default]'),
options_lookup['output_dir']
]

script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    matplotlib_version = re.split("[^\d]", matplotlib.__version__)
    matplotlib_version_info = tuple([int(i) for i in matplotlib_version if \
                            i.isdigit()])

    if matplotlib_version_info != (0,98,5,3) and \
        matplotlib_version_info != (0,98,5,2):
        print "This code was only tested with Matplotlib-0.98.5.2 and \
              Matplotlib-0.98.5.3"
    data = {}

    prefs,data,background_color,label_color= \
                            sample_color_prefs_and_map_data_from_options(opts)

    #Open and get coord data
    data['coord'] = get_coord(opts.coord_fname)

    filepath=opts.coord_fname
    filename=filepath.strip().split('/')[-1]

    qiime_dir=get_qiime_project_dir()

    js_path=os.path.join(qiime_dir,'qiime','support_files','js')

    if opts.output_dir:
        if os.path.exists(opts.output_dir):
            dir_path=opts.output_dir
        else:
            try:
                os.mkdir(opts.output_dir)
                dir_path=opts.output_dir
            except OSError:
                pass
    else:
        dir_path='./'
        
    html_dir_path=dir_path
    data_dir_path = get_random_directory_name(output_dir=dir_path)
    
    try:
        os.mkdir(data_dir_path)
    except OSError:
        pass

    js_dir_path = os.path.join(html_dir_path,'js')
    try:
        os.mkdir(js_dir_path)
    except OSError:
        pass

    shutil.copyfile(os.path.join(js_path,'overlib.js'), \
                                    os.path.join(js_dir_path,'overlib.js'))

    try:
        action = generate_2d_plots
    except NameError:
        action = None
    #Place this outside try/except so we don't mask NameError in action
    if action:
        action(prefs,data,html_dir_path,data_dir_path,filename,background_color,
                label_color)


if __name__ == "__main__":
    main()