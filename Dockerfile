

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
#the command above prevents install applications from asking questions using a GUI interface

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y apt-utils
#RUN apt-get install dialog apt-utils -y



#RUN apt-get upgrade -y

#RUN apt-get update
#RUN apt-get install -y vim
#RUN apt-get update
#RUN apt-get install -y python3.8
#RUN apt-get update
RUN apt-get install -y python3-pip 
#RUN apt-get update
#RUN apt-get install -y iputils-ping
#RUN apt-get update
#RUN apt-get install -y astrometry.net
RUN apt-get install -y sextractor



#RUN apt install -y astrometry.net

RUN echo 'alias python="/usr/bin/python3.10"' >> /root/.bashrc


RUN pip3 install psycopg2-binary
RUN pip3 install numpy
RUN pip3 install scipy
RUN pip3 install scipy --upgrade
#scipy is causing an error with numpy verision. the default install is no update to date so forceing an update which is working
RUN pip3 install matplotlib
RUN pip3 install astropy
RUN pip3 install photutils
#RUN pip3 install numba



#we are going to make the dir DAP here then make that the workingDir. This need to occur now because not until after the DockerFile is build are the volumne connected
#RUN mkdir /dap
#RUN mkdir /dap/c_source_extract
#the below is the source_extractor files
#RUN mkdir /dap/c_source_extract/sex
#RUN mkdir /dap/c_source_extract/src
WORKDIR /dap/c_sources/src 



#COPY /src/source_extractor.py /dap/c_source_extract/src/source_extractor.py
#COPY /src/keepRunning.py /dap/c_source_extract/src/keepRunning.py
#COPY /src/default.conv /dap/c_source_extract/src/default.conv
#COPY /src/default.param /dap/c_source_extract/src/default.param

#COPY /src/photutil_aperture.py /dap/c_source_extract/src/photutil_aperture.py
#COPY /src/photutil_detection.py /dap/c_source_extract/src/photutil_detection.py
#COPY /src/photutil_ePSF_builder.py /dap/c_source_extract/src/photutil_ePSF_builder.py
#COPY /src/photutil_main.py /dap/c_source_extract/src/photutil_main.py
#COPY /src/photutil_psf.py /dap/c_source_extract/src/photutil_psf.py

#COPY /src/client_queue.py /dap/c_source_extract/src/client_queue.py
#COPY /src/log.py /dap/c_source_extract/src/log.py

#COPY /src/tphot /dap/c_source_extract/src/tphot

#COPY pythonServer.py /pythonServer.py
#COPY bashFile.sh /bashFile.sh
#this is to test if permission will work
#COPY sqs_test.py /sqs_test.py 
#COPY config /config

#RUN chmod +x /bashFile.sh
#RUN chmod +x /dap/c_source_extract/src/source_extractor.py
#RUN chmod +x /dap/c_source_extract/src/keepRunning.py

#RUN ./baseFile.sh
#RUN ./dap/a_start_up/src/start_up.py

#RUN ["chmod", "+x", "/bashFile.sh"]
#ENTRYPOINT [ "/bashFile.sh"]
#ENTRYPOINT ["/dap/a_start_up/src/start_up.py"]

#CMD ["python3.8", "/dap/c_source_extract/src/source_extractor.py"]
#CMD ["python3.8", "/dap/c_source_extract/src/keepRunning.py"]

#RUN ["chmod", "+x", "/dap/a_start_up/src/start_up.py"] #change permission of file
#ENTRYPOINT ["python", "/dap/a_start_up/src/start_up.py"]
#ENTRYPOINT ["python3.8", "start_up.py"] #I assume if the workdir is already there



#CMD python --version


#CMD ["apache2ctl", "-D", "FOREGROUND"]

