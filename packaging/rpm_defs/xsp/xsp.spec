
# norootforbuild

Name:           xsp
URL:            http://go-mono.com/
License:        GNU General Public License (GPL)
Group:          Productivity/Networking/Web/Servers
Autoreqprov:    on
Version:        1.2.4
Release:        1
Summary:        Small Web Server Hosting ASP.NET
Source:         %{name}-%{version}.tar.bz2
#Patch:        xsp-libexecdir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch: noarch

BuildRequires:  mono-devel mono-web pkgconfig

#####  suse  ####
%if 0%{?suse_version}

%define old_suse_buildrequires mono-data mono-winforms

%if %suse_version == 1000
BuildRequires:  %{old_suse_buildrequires}
%endif

%if %sles_version == 9
BuildRequires:  %{old_suse_buildrequires}
%endif

%endif

# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif


%description
The XSP server is a small Web server that hosts the Mono System.Web
classes for running what is commonly known as ASP.NET.


%debug_package
%prep
%setup -q

%build
%{?env_options}
# Cannot use the configure macro because noarch-redhat-linux is not recognized by the auto tools in the tarball
./configure --prefix=%{_prefix} \
	    --libexecdir=%{_prefix}/lib \
	    --libdir=%{_prefix}/lib \
	    --mandir=%{_prefix}/share/man \
	    --infodir=%{_prefix}/share/info \
	    --sysconfdir=%{_sysconfdir}
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/usr/share
mv ${RPM_BUILD_ROOT}/usr/lib/pkgconfig ${RPM_BUILD_ROOT}/usr/share

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/share/pkgconfig/*
%{_prefix}/share/man/*/*
%{_prefix}/lib/xsp
%{_prefix}/lib/mono/gac/Mono.WebServer
%{_prefix}/lib/mono/1.0/Mono.WebServer.dll
%{_prefix}/lib/mono/gac/Mono.WebServer2
%{_prefix}/lib/mono/2.0/Mono.WebServer2.dll
%{_prefix}/lib/mono/gac/xsp
%{_prefix}/lib/mono/1.0/xsp.exe
%{_prefix}/lib/mono/gac/xsp2
%{_prefix}/lib/mono/2.0/xsp2.exe
%{_prefix}/lib/mono/gac/mod-mono-server
%{_prefix}/lib/mono/1.0/mod-mono-server.exe
%{_prefix}/lib/mono/gac/mod-mono-server2
%{_prefix}/lib/mono/2.0/mod-mono-server2.exe
%doc NEWS README

# auto dep/req generation for older distros (it will take a while for the .config scanning to get upstream)
%if 0%{?suse_version} <= 1040 || 0%{?fedora_version} <= 7
%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'
%endif

%changelog
