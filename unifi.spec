%global debug_package %{nil}
%define __jar_repack %{nil}

Name:           unifi
Version:        5.14.22
Release:        1%{?dist}
Summary:        Ubiquiti UniFi controller
License:        Proprietary
URL:            https://unifi-sdn.ubnt.com/
ExclusiveArch:  x86_64 aarch64

Source0:        http://dl.ubnt.com/%{name}/%{version}/UniFi.unix.zip#/UniFi-%{version}.unix.zip
Source1:        %{name}.service
Source3:        %{name}.xml
Source4:        %{name}.logrotate

Source10:       https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.18.tgz
Source11:       https://fastdl.mongodb.org/linux/mongodb-linux-arm64-ubuntu1604-4.0.18.tgz

Obsoletes:      %{name}-data < %{version}
Obsoletes:      %{name}-mongodb < %{version}

BuildRequires:  firewalld-filesystem
BuildRequires:  %{_bindir}/execstack
BuildRequires:  systemd

Requires:       firewalld-filesystem
Requires:       java-1.8.0-openjdk-headless
Requires:       logrotate
%{?systemd_requires}
Requires(pre):  shadow-utils

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

%description
Ubiquiti UniFi server is a centralized management system for UniFi suite of
devices. After the UniFi server is installed, the UniFi controller can be
accessed on any web browser. The UniFi controller allows the operator to
instantly provision thousands of UniFi devices, map out network topology,
quickly manage system traffic, and further provision individual UniFi devices.

%prep
%autosetup -n UniFi

# Remove bundled fontawesome font
rm -f webapps/ROOT/app-unifi/fonts/*.{ttf,eot,otf,svg,woff,woff2}

# Replace empty symlink with mongod executable
rm -fr bin
%ifarch x86_64
tar -xvz --strip-component=1 --no-anchored -f %{SOURCE10} */bin/mongod
%endif
%ifarch aarch64
tar -xvz --strip-component=1 --no-anchored -f %{SOURCE11} */bin/mongod
%endif

# Strip binaries for which we have no source matching in the package build
strip bin/mongod lib/native/Linux/%{_arch}/*.so

# Try to fix java VM warning about running execstack on libubnt_webrtc_jni.so
execstack -c lib/native/Linux/%{_arch}/libubnt_webrtc_jni.so

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -a ./{bin,conf,dl,lib,webapps} %{buildroot}%{_libdir}/%{name}/

# Remove non-native executables and fix permissions
rm -rf lib/native/{Windows,Mac}
shopt -s extglob
rm -rf %{buildroot}%{_libdir}/%{name}/lib/native/Linux/!(%{_arch})
shopt -u extglob
chmod 755 %{buildroot}%{_libdir}/%{name}/lib/native/Linux/%{_arch}/*.so

# Create data folders
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/{data,run,work}
ln -sf %{_sharedstatedir}/%{name}/data \
    %{buildroot}%{_libdir}/%{name}/data
ln -sf %{_sharedstatedir}/%{name}/run \
    %{buildroot}%{_libdir}/%{name}/run
ln -sf %{_sharedstatedir}/%{name}/work \
    %{buildroot}%{_libdir}/%{name}/work

# Create log folder
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
ln -sf %{_localstatedir}/log/%{name} \
       %{buildroot}%{_libdir}/%{name}/logs

# Install systemd service file
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# Install firewalld config
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services
install -pm 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/firewalld/services/

# Install logrotate config
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "Ubiquiti UniFi Controller" %{name}
exit 0

%post
%systemd_post %{name}.service
%{?firewalld_reload}

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%{?firewalld_reload}

%files
%doc readme.txt
%{_libdir}/%{name}/
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}.service
%{_prefix}/lib/firewalld/services/%{name}.xml
%ghost %attr(-,%{name},%{name}) %config(missingok,noreplace) %{_sharedstatedir}/%{name}/data/system.properties
%attr(-,%{name},%{name}) %{_localstatedir}/log/%{name}/
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}/data
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}/run
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}/work

%changelog
* Fri Aug 21 2020 Simone Caronni <negativo17@gmail.com> - 5.14.22-1
- Update to 5.14.22.

* Sun Aug 16 2020 Simone Caronni <negativo17@gmail.com> - 5.13.32-2
- Use explicit java package dependency.

* Thu Jul 09 2020 Simone Caronni <negativo17@gmail.com> - 5.13.32-1
- Update to 5.13.32.

* Wed Jun 17 2020 Simone Caronni <negativo17@gmail.com> - 5.13.29-1
- Update to 5.13.29.

* Fri May 22 2020 Simone Caronni <negativo17@gmail.com> - 5.12.72-2
- Bundle MongoDB binary version 4.0 (interim step to upgrade to 4.2).
- Remove external unifi-mongodb package requirement.
- Keep only native binaries and strip them as the source is not available for
  generating debug packages.
- Add missing logrotate dependency and mark config file.
- Allow building also for aarch64.

* Thu May 21 2020 Simone Caronni <negativo17@gmail.com> - 5.12.72-1
- Update to 5.12.72.

* Wed Apr 01 2020 Simone Caronni <negativo17@gmail.com> - 5.12.66-1
- Update to 5.12.66.

* Fri Feb 21 2020 Simone Caronni <negativo17@gmail.com> - 5.12.35-4
- Remove Python SELinux dependency.

* Mon Dec 02 2019 Simone Caronni <negativo17@gmail.com> - 5.12.35-3
- Fix library permissions.

* Mon Dec 02 2019 Simone Caronni <negativo17@gmail.com> - 5.12.35-2
- Remove spurious symlink for mongod.

* Sun Dec 01 2019 Simone Caronni <negativo17@gmail.com> - 5.12.35-1
- Update to 5.12.35.

* Sun Oct 20 2019 Simone Caronni <negativo17@gmail.com> - 5.11.50-1
- Update to 5.11.50.
- Require a private MongoDB.
- Remove ARM conditionals.
- Simplify packaging.

* Tue Sep 03 2019 Simone Caronni <negativo17@gmail.com> - 5.11.39-1
- Update to 5.11.39.

* Fri Jul 19 2019 Simone Caronni <negativo17@gmail.com> - 5.10.25-1
- Update to 5.10.25.

* Sun May 26 2019 Simone Caronni <negativo17@gmail.com> - 5.10.23-1
- Update to 5.10.23.

* Sat Apr 06 2019 Simone Caronni <negativo17@gmail.com> - 5.10.20-1
- Update to 5.10.20.

* Sat Mar 09 2019 Simone Caronni <negativo17@gmail.com> - 5.10.19-1
- Update to 5.10.19.

* Sat Feb 23 2019 Simone Caronni <negativo17@gmail.com> - 5.10.17-1
- Update to 5.10.17.

* Sun Feb 10 2019 Simone Caronni <negativo17@gmail.com> - 5.10.12-1
- Update to 5.10.12.
- Trim changelog.
- Hardcode Java 1.8.0 version in requirements and systemd unit.

* Tue Nov 13 2018 Richard Shaw <hobbes1069@gmail.com> - 5.9.29-2
- Update systemd service file to deal with Java 10 in F29+, fixes BZ#5080.
