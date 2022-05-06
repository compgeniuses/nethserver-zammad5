Summary: NethServer zammad5 integration
Name: nethserver-zammad5
Version: 1.0.0
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
Source0: %{name}-%{version}.tar.gz
%define composeVersion 2.5.0
Source1: https://github.com/docker/compose/releases/download/v%{composeVersion}/docker-compose-linux-x86_64
Source2: https://github.com/zammad/zammad-docker-compose/archive/refs/heads/master.zip
BuildArch: noarch

Requires: nethserver-docker, curl, git
# nethserver-nginx, nethserver-postgresql, java-1.8.0-openjdk, elasticsearch, zammad

BuildRequires: perl
BuildRequires: nethserver-devtools

%description
NethServer Zammad 5 integration

%prep
%setup

%build
perl createlinks
mkdir -p root/var/lib/nethserver/zammad5/backup

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/%{name}/

cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a ui/* %{buildroot}/usr/share/cockpit/%{name}/

mkdir -p %{buildroot}/opt/zammad-docker-compose
mv %SOURCE1 %{buildroot}/opt/zammad-docker-compose/docker-compose

unzip %SOURCE2 "zammad-docker-compose-master/*" -d "%{buildroot}/opt/zammad-docker-compose"

(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} \
%{buildroot} > %{name}-%{version}-filelist

#  --dir /var/lib/nethserver/zammad5/backup 'attr(755, root, root)' \
#  --file /etc/sudoers.d/50_nsapi_nethserver_zammad5 'attr(0440,root,root)' \
#  --file /usr/libexec/nethserver/api/%{name}/read 'attr(775,root,root)' \


%post

%preun

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%attr(0755,root,root) /opt/zabbix-docker/docker-compose
%doc COPYING
%dir %{_nseventsdir}/%{name}-update

%changelog
* Sun Feb 20 2022 Markus Neuberger <info@markusneuberger.at> - 0.0.1-1
- Initial Release
