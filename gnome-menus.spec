Summary:	Implementation of the draft Desktop Menu Specification
Summary(pl):	Implementacja specyfikacji menu system�w biurkowych
Name:		gnome-menus
Version:	2.10.0
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-menus/2.10/%{name}-%{version}.tar.bz2
# Source0-md5:	7c0776f79dcd08de97de2b6f9c17c830
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.6.1
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	intltool >= 0.31
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
Provides:	applnk = 1.9.4
Obsoletes:	applnk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec .

%description -l pl
Pakiet zawiera implementacj� specyfikacji menu system�w biurkowych z
freedesktop.org: http://www.freedesktop.org/Standards/menu-spec .

%package libs
Summary:	gnome-menus library
Summary(pl):	Biblioteka gnome-menus
Group:		Libraries
Requires:	applnk >= 1.9.4
Obsoletes:	gnome-vfs2-module-menu

%description libs
gnome-menus library.

%description libs -l pl
Biblioteka gnome-menus.

%package devel
Summary:	Header files of gnome-menus library
Summary(pl):	Pliki nag��wkowe biblioteki gnome-menus
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.6.1

%description devel
Headers for gnome-menus library.

%description devel -l pl
Pliki nag��wkowe biblioteki gnome-menus.

%package static
Summary:	Static gnome-menus library
Summary(pl):	Statyczna biblioteka gnome-menus
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of gnome-menu library.

%description static -l pl
Statyczna biblioteka gnome-menu.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/xdg/menus
%{_datadir}/desktop-directories

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnome-menu.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_pkgconfigdir}/*.pc
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
