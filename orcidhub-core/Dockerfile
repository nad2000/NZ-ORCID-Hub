FROM centos:centos7

LABEL maintainer="The University of Auckland" \
	version="?" \
	description="NZ ORCiD Hub Application Image with Development support"

ADD http://download.opensuse.org/repositories/security://shibboleth/CentOS_7/security:shibboleth.repo /etc/yum.repos.d/shibboleth.repo

COPY conf/app.wsgi /var/www/html/
# prefix "ZZ" added, that it gest inluded the very end (after Shibboleth gets loaded)
COPY conf/app.conf /etc/httpd/conf.d/ZZ-app.conf
COPY requirements.txt /requirements.txt
COPY run-app /usr/local/bin/
COPY ./conf /conf

RUN yum -y update \ 
    && yum -y install https://centos7.iuscommunity.org/ius-release.rpm \
    && yum -y install \
    	shibboleth.x86_64 \
    	httpd \
	mod_ssl \
    	gcc.x86_64 \
        httpd-devel.x86_64 \
	python36u.x86_64 \
	python36u-devel.x86_64 \
	python36u-pip \
    && pip3.6 install mod_wsgi psycopg2 \
    && pip3.6 install -r /requirements.txt \
    && rm -f /requirements.txt \
    && /usr/bin/mod_wsgi-express module-config >/etc/httpd/conf.modules.d/10-wsgi.conf \
    && [ -d /var/run/lock ] || mkdir -p /var/run/lock \
    && [ -d /var/lock/subsys/ ] || mkdir -p /var/lock/subsys/ \
    && echo $'export LD_LIBRARY_PATH=/opt/shibboleth/lib64:$LD_LIBRARY_PATH\n' > /etc/sysconfig/shibd \
    && chmod +x /etc/sysconfig/shibd /etc/shibboleth/shibd-redhat \
    && yum erase -y \
	apr-util-devel \
	cpp \
	cyrus-sasl-devel \
	expat-devel \
	gcc \
	glibc-devel \
	glibc-headers \
	httpd-devel \
	kernel-headers \
	libdb-devel \
	openldap-devel \
	perl \
	python36u-devel \
	python36u-pip \
    && chmod +x /usr/local/bin/run-app \
    && cd /var/lib/rpm \
    && rm -rf __db* \
    && rpm --rebuilddb \
    && yum -y clean all \
    && rm -rf $HOME/.pip/cache \
    && rm -rf /var/cache/*/* /anaconda-post.log

EXPOSE 80 443

CMD ["run-app"]
