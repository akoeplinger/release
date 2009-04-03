%define real_name libgdiplus

Name:           libgdiplus0
Version:        2.4
Release:        0
License:        LGPL v2.1 only; MOZILLA PUBLIC LICENSE (MPL/NPL); X11/MIT
Url:            http://go-mono.org/
Source0:        %{real_name}-%{version}.tar.bz2
Summary:        Open Source Implementation of the GDI+ API
Group:          Development/Libraries/Other
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Obsoletes:      libgdiplus-devel
Provides:       libgdiplus-devel
Obsoletes:      libgdiplus
Provides:       libgdiplus
####  suse  ####
%if 0%{?suse_version}
# Common requires for suse distros
BuildRequires:  fontconfig-devel freetype2-devel glib2-devel libexif libjpeg-devel libpng-devel libtiff-devel
%if %suse_version >= 1030
BuildRequires:  giflib-devel libexif-devel xorg-x11-libSM-devel xorg-x11-libXrender-devel
%endif
%if %suse_version == 1020
BuildRequires:  giflib-devel xorg-x11-libSM-devel xorg-x11-libXrender-devel
%endif
%if %sles_version == 10
BuildRequires:  giflib-devel xorg-x11-devel
%endif
%if %suse_version == 1010
BuildRequires:  giflib-devel xorg-x11-devel
%endif
%if %sles_version == 9
BuildRequires:  XFree86-devel libungif pkgconfig
%endif
%endif
####  fedora  ####
%if 0%{?fedora_version}
# All fedora distros have the same names, requirements
BuildRequires:  fontconfig-devel glib2-devel libXrender-devel libXt-devel libexif-devel libjpeg-devel libpng-devel libtiff-devel libungif-devel
%endif
%if 0%{?rhel_version}
BuildRequires:  fontconfig-devel glib2-devel libexif-devel libjpeg-devel libpng-devel libtiff-devel libungif-devel
%if %{rhel_version} >= 500
BuildRequires:  libXrender-devel libXt-devel
%endif
%endif

%description
This is part of the Mono project. It is required when using
Windows.Forms.



Authors:
--------
    Alexandre Pigolkine
    Duncan Mak
    Jordi Mas
    Miguel de Icaza
    Ravindra Kumar

%files
%defattr(-, root, root)
%_libdir/libgdiplus.so*
%_libdir/pkgconfig/libgdiplus.pc
%doc AUTHORS COPYING ChangeLog* NEWS README

%prep
%setup -q -n %{real_name}-%{version}

%build
# Set PKG_CONFIG_PATH for sles9
%if 0%{?sles_version}
%if %sles_version == 9
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
%endif
%endif
export CFLAGS="$RPM_OPT_FLAGS"
%configure
make

%install
make install DESTDIR=%{buildroot}
# Unwanted files:
rm -f %{buildroot}%{_libdir}/libgdiplus.a
rm -f %{buildroot}%{_libdir}/libgdiplus.la
# Remove generic non-usefull INSTALL file... (appeases
#  suse rpmlint checks, saves 3kb)
find . -name INSTALL | xargs rm -f

%clean
rm -rf "$RPM_BUILD_ROOT"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
