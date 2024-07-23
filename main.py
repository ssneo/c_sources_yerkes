import os, sys


os.system("docker stop c_source_yerkes")
os.system("docker rm c_source_yerkes")


os.system("docker image rm c_source_yerkes")


os.system("docker build . --platform linux/x86_64 -t c_source_yerkes")

#os.system("docker push tylerlinder/c_source_extractor_rev_1")

#os.system("docker run -t -d --platform linux/amd64 -v ~/research/dap:/dap -v ~/research/dap_data:/dap_data -v ~/research/dap/c_sources_yerkes/cfg:/dap/c_source_extract/cfg --name c_source_yerkes c_source_yerkes")
os.system("docker run -t -d --platform linux/amd64 -v ~/research/dap:/dap -v ~/research/dap_data:/dap_data --name c_source_yerkes c_source_yerkes")
#
#if sys.platform == 'darwin':
#    os.system("docker run -t -d --platform linux/x86_64 -v ~/research/dap:/dap -v ~/research/dap_data:/dap_data -v ~/research/dap/c_source_extract/sex:/dap/c_source_extract/sex --name c_source_extractor c_source_extractor")
#else:
#    os.system("docker run -d -v C:\\Users\\tlind\\research\\dap:/dap -v C:\\Users\\tlind\\research\\dap_data:/dap_data C:\\Users\\tlind\\research\\dap_index_files:/dap_index_files --name dap dap")
os.system("docker exec -it c_source_yerkes bash")

#os.system("docker run -it -v ~/research/dap:/dap -v ~/research/dap_data:/dap_data --name dap dap")