############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 2013 Xilinx Inc. All rights reserved.
############################################################
open_project sad
set_top sad
add_files sad.cpp
open_solution "solution1"
set_part {xc7z010clg225-2}
create_clock -period 10 -name default
source "./sad/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design -trace_level none
export_design -format ip_catalog -description "An IP generated by Vivado HLS" -vendor "xilinx.com" -library "hls" -version "1.0"
