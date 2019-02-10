# This is a binary package so debuginfo doesn't do anything useful.
%global debug_package %{nil}
%define __jar_repack %{nil}
%global __strip /bin/true

Name:           unifi
Version:        5.10.12
Release:        1%{?dist}
Summary:        Ubiquiti UniFi controller

License:        Proprietary
URL:            https://unifi-sdn.ubnt.com/
Source0:        http://dl.ubnt.com/%{name}/%{version}/UniFi.unix.zip#/UniFi-%{version}.unix.zip
Source1:        %{name}.service
Source3:        %{name}.xml
Source4:        %{name}.logrotate
Source6:        mongod.sh
Source102:      SETUP

%{?systemd_requires}

Requires(pre):  shadow-utils
Requires:       firewalld-filesystem

BuildRequires:  firewalld-filesystem
BuildRequires:  %{_bindir}/execstack

Requires:       mongodb-server
Requires:       java-headless == 1:1.8.0
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

# Unbundled fonts
Requires:       fontawesome-fonts
Requires:       fontawesome-fonts-web

# https://bugzilla.redhat.com/show_bug.cgi?id=1517565
Provides:       bundled(lato-fonts-web)
Provides:       bundled(ubnt-fonts)

# Bundled java libraries
# This needs to be automated!
Provides:       bundled(annotations) = 2.0.0
Provides:       bundled(aws-java-sdk-cloudwatch) = 1.9.3
Provides:       bundled(aws-java-sdk-core) = 1.9.3
Provides:       bundled(aws-java-sdk-s3) = 1.9.3
Provides:       bundled(commons-beanutils) = 1.9.1
Provides:       bundled(commons-codec) = 1.7
Provides:       bundled(commons-httpclient) = 3.1
Provides:       bundled(commons-httpclient-contrib) = 3.1
Provides:       bundled(commons-io) = 2.4
Provides:       bundled(commons-lang) = 2.6
Provides:       bundled(commons-logging) = 1.1.3
Provides:       bundled(commons-net) = 3.3
Provides:       bundled(commons-pool2) = 2.2
Provides:       bundled(commons-validator) = 1.5.0
Provides:       bundled(compiler) = 0.8.18
Provides:       bundled(cron4j) = 2.2.5
Provides:       bundled(dom4j) = 1.3
Provides:       bundled(ecj) = 4.3.1
Provides:       bundled(gson) = 2.2.4
Provides:       bundled(guava) = 14.0.1
Provides:       bundled(httpclient) = 4.2
Provides:       bundled(httpcore) = 4.2
Provides:       bundled(jackson-annotations) = 2.1.1
Provides:       bundled(jackson-core) = 2.1.1
Provides:       bundled(jackson-databind) = 2.1.1
Provides:       bundled(Java-WebSocket) = 1.3.0
Provides:       bundled(jedis) = 2.8.1
Provides:       bundled(jmdns) = 3.4.1
Provides:       bundled(joda-time) = 2.9.4
Provides:       bundled(jorbis) = 0.0.17
Provides:       bundled(jsch) = 0.1.51
Provides:       bundled(jstl) = 1.2
Provides:       bundled(jstun) = 0.7.3
Provides:       bundled(jul-to-slf4j) = 1.7.6
Provides:       bundled(log4j) = 1.2.17
Provides:       bundled(mail) = 1.4.7
Provides:       bundled(mongo-java-driver) = 2.14.3
Provides:       bundled(radclient4)
Provides:       bundled(servo-core) = 0.9.4
Provides:       bundled(servo-graphite) = 0.9.4
Provides:       bundled(slf4j-api) = 1.7.6
Provides:       bundled(slf4j-log4j12) = 1.7.6
Provides:       bundled(snappy-java) = 1.1.2.6
Provides:       bundled(spring-beans) = 3.2.8
Provides:       bundled(spring-context) 3.2.8
Provides:       bundled(spring-core) = 3.2.8
Provides:       bundled(spring-expression) = 3.2.8
Provides:       bundled(spring-test) = 3.2.8
Provides:       bundled(sshj) = 0.9.0
Provides:       bundled(tomcat-annotations-api) = 7.0.82
Provides:       bundled(tomcat-embed-core) =  7.0.82
Provides:       bundled(tomcat-embed-el) = 7.0.82
Provides:       bundled(tomcat-embed-jasper) = 7.0.82
Provides:       bundled(tomcat-embed-logging-juli) = 7.0.82
Provides:       bundled(tomcat-embed-logging-log4j) = 7.0.82
Provides:       bundled(urlrewritefilter) = 4.0.4

# So you can prevent automatic updates.
%if 0%{?fedora}
Recommends:     dnf-plugin-versionlock
%endif

Requires:       %{name}-data = %{version}-%{release}

%description
Ubiquiti UniFi server is a centralized management system for UniFi suite of
devices. After the UniFi server is installed, the UniFi controller can be
accessed on any web browser. The UniFi controller allows the operator to
instantly provision thousands of UniFi devices, map out network topology,
quickly manage system traffic, and further provision individual UniFi devices.

%package data
BuildArch:      noarch
Summary:        Non-architechture specific data files for unifi

%description data
Non-architechture specific data files for the unifi controller software.

%prep
%autosetup -n UniFi

install -pm 0644 %{SOURCE102} .

# Unbundle fontawesome fot
rm -f webapps/ROOT/app-unifi/fonts/*.{ttf,eot,otf,svg,woff,woff2}

%install
# Install into /usr/share/unifi
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a ./*  %{buildroot}%{_datadir}/%{name}/

# Remove readme as it will be handled by %%doc
rm -f %{buildroot}%{_datadir}/%{name}/readme.txt

### Attempt a more FHS compliant install...
# Create directories for live data and symlink it into /usr/share so unifi
# can find them.
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/{data,run,work}
ln -sr %{buildroot}%{_sharedstatedir}/%{name}/data \
       %{buildroot}%{_datadir}/%{name}/data
ln -sr %{buildroot}%{_sharedstatedir}/%{name}/run \
       %{buildroot}%{_datadir}/%{name}/run
ln -sr %{buildroot}%{_sharedstatedir}/%{name}/work \
       %{buildroot}%{_datadir}/%{name}/work

# Create logs in /var/log and symlink it in.
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
ln -sr %{buildroot}%{_localstatedir}/log/%{name} \
       %{buildroot}%{_datadir}/%{name}/logs

# Install systemd service file
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# Install firewalld config
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services
install -pm 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/firewalld/services/

# Remove non-native executables
rm -rf %{buildroot}%{_datadir}/%{name}/lib/native/{Windows,Mac}

# Bundled libs are only supported on x86_64, aarch64 and armv7hf.
# Move libraries to the correct location and symlink back
mv %{buildroot}%{_datadir}/%{name}/lib/native/Linux ./
%ifarch x86_64 armv7hl aarch64
# Set the correct arch for the webrtc library.
%ifarch armv7hl
%global unifi_arch armv7
%else 
%global unifi_arch %{_target_cpu}
%endif
mkdir -p %{buildroot}%{_libdir}/%{name} \
         %{buildroot}%{_datadir}/%{name}/lib/native/Linux/%{unifi_arch}
install -pm 0755 Linux/%{unifi_arch}/*.so %{buildroot}%{_libdir}/%{name}/
for lib in $(ls %{buildroot}%{_libdir}/%{name}/*.so); do
    ln -sr $lib %{buildroot}%{_datadir}/%{name}/lib/native/Linux/%{unifi_arch}
done
# Try to fix java VM warning about running execstack on libubnt_webrtc_jni.so
find %{buildroot}%{_libdir} -name libubnt_webrtc_jni.so -exec execstack -c {} \;
%endif

# Install logrotate config
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Workaround script for MongoDB 3.6 no longer accepting --nohttpinterface.
# See: https://community.ubnt.com/t5/UniFi-Routing-Switching/MongoDB-3-6/m-p/2322445#M86254
#
%if 0%{?fedora} >= 28
    install -pm 0755 %{SOURCE6} %{buildroot}%{_datadir}/%{name}/bin/mongod
%endif

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "Ubiquitu UniFi Controller" %{name}
exit 0

%post
%systemd_post %{name}.service
%{?firewalld_reload}
# Set required SELinux context for unifi to use a private mongodb database.
%if "%{_selinux_policy_version}" != ""
    semanage fcontext -a -t mongod_log_t \
        "%{_localstatedir}/log/%{name}(/.*)?" 2>/dev/null || :
    semanage fcontext -a -t mongod_var_lib_t \
        "%{_sharedstatedir}/%{name}/data(/.*)?" 2>/dev/null || :
    restorecon -R %{_localstatedir}/log/%{name} \
                  %{_sharedstatedir}/%{name}/data || :
    semanage port -a -t mongod_port_t -p tcp 27117 2>/dev/null || :
%endif

%preun
%systemd_preun %{name}.service

%postun
# Restart the service on upgrade.
%systemd_postun_with_restart %{name}.service
# Remove selinux modifications on uninstall
if [ $1 -eq 0 ] ; then  # final removal
%if "%{_selinux_policy_version}" != ""
    semanage fcontext -d -t mongod_log_t \
        "%{_localstatedir}/log/%{name}(/.*)?" 2>/dev/null || :
    semanage fcontext -d -t mongod_var_lib_t \
        "%{_sharedstatedir}/%{name}/data(/.*)?" 2>/dev/null || :
    semanage port -d -t mongod_port_t -p tcp 27117 2>/dev/null || :
%endif
fi

%files
%doc readme.txt SETUP
%ifarch x86_64 armv7hl aarch64
%{_libdir}/%{name}/
%{_datadir}/%{name}/lib/native/
%endif
%{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}.service
%{_prefix}/lib/firewalld/services/%{name}.xml
%ghost %attr(-,%{name},%{name}) %config(missingok,noreplace) %{_sharedstatedir}/%{name}/data/system.properties
%attr(-,%{name},%{name}) %{_localstatedir}/log/%{name}/
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}/data
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}/run
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}/work

%files data
%exclude %{_datadir}/%{name}/lib/native
%{_datadir}/%{name}/


%changelog
* Sun Feb 10 2019 Simone Caronni <negativo17@gmail.com> - 5.10.12-1
- Update to 5.10.12.
- Trim changelog.
- Hardcode Java 1.8.0 version in requirements and systemd unit.

* Tue Nov 13 2018 Richard Shaw <hobbes1069@gmail.com> - 5.9.29-2
- Update systemd service file to deal with Java 10 in F29+, fixes BZ#5080.
