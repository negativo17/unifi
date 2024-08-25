%global debug_package %{nil}
%define __jar_repack %{nil}
%global hash y2b2oj1o96

Name:           unifi
Version:        8.4.59
Release:        1%{?dist}
Summary:        Ubiquiti UniFi controller
License:        Proprietary
URL:            https://ui.com/
ExclusiveArch:  x86_64 aarch64

Source0:        https://dl.ui.com/%{name}/%{version}%{?hash:-%{hash}}/UniFi.unix.zip#/UniFi.unix.%{version}.zip
Source1:        %{name}.service
Source3:        %{name}.xml
Source4:        %{name}.logrotate

Source10:       https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel90-7.0.12.tgz
Source11:       https://fastdl.mongodb.org/linux/mongodb-linux-aarch64-rhel90-7.0.12.tgz

Obsoletes:      %{name}-data < %{version}
Obsoletes:      %{name}-mongodb < %{version}

BuildRequires:  firewalld-filesystem
BuildRequires:  systemd

Requires:       firewalld-filesystem
Requires:       java-17-openjdk-headless
Requires:       logrotate
%{?systemd_requires}
Requires(pre):  shadow-utils

%description
Ubiquiti UniFi server is a centralized management system for UniFi suite of
devices. After the UniFi server is installed, the UniFi controller can be
accessed on any web browser. The UniFi controller allows the operator to
instantly provision thousands of UniFi devices, map out network topology,
quickly manage system traffic, and further provision individual UniFi devices.

%prep
%autosetup -n UniFi

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
* Sun Aug 25 2024 Simone Caronni <negativo17@gmail.com> - 8.4.59-1
- Update to 8.4.59.
- Update MongoDB to 7.0.12.

* Fri Jun 14 2024 Simone Caronni <negativo17@gmail.com> - 8.2.93-1
- Update to 8.2.93.

* Mon Apr 29 2024 Simone Caronni <negativo17@gmail.com> - 8.1.127-1
- Update to 8.1.127.
- Update MongoDB to 7.0.9.
- Trim changelog.

* Thu Mar 21 2024 Simone Caronni <negativo17@gmail.com> - 8.1.113-2
- Update to 8.1.113.

* Sat Jan 06 2024 Simone Caronni <negativo17@gmail.com> - 8.0.26-1
- Update to 8.0.26.

* Tue Dec 19 2023 Simone Caronni <negativo17@gmail.com> - 8.0.24-1
- Update to 8.0.24.

* Tue Nov 21 2023 Simone Caronni <negativo17@gmail.com> - 8.0.7-1
- Update to 8.0.7.

* Wed Nov 08 2023 Simone Caronni <negativo17@gmail.com> - 8.0.6-1
- Update to 8.0.6.

* Tue Oct 31 2023 Simone Caronni <negativo17@gmail.com> - 7.5.187-1
- Update to 7.5.187.
- Trim changelog.

* Fri Sep 29 2023 Simone Caronni <negativo17@gmail.com> - 7.5.176-1
- Update to 7.5.176.

* Tue Sep 05 2023 Simone Caronni <negativo17@gmail.com> - 7.5.174-1
- Update to 7.5.174.

* Mon Jul 10 2023 Simone Caronni <negativo17@gmail.com> - 7.4.162-1
- Update to 7.4.162.

* Wed May 24 2023 Simone Caronni <negativo17@gmail.com> - 7.4.156-2
- Update to 7.4.156.

* Wed May 10 2023 Simone Caronni <negativo17@gmail.com> - 7.4.154-1
- Update to 7.4.154.

* Mon Feb 6 2023 Brian Likosar <bjlikosar@gmail.com> - 7.3.83-1
- Update to 7.3.83.
- Change depedency to Java 11 from deprecated Java 8.
