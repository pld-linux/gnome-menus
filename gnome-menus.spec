Summary:	Implementation of the draft Desktop Menu Specification
Summary(pl):	Implementacja specyfikacji menu system�w biurkowych
Name:		gnome-menus
Version:	2.13.5
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-menus/2.13/%{name}-%{version}.tar.bz2
# Source0-md5:	07083058ce27a2132bc3f578c055fff6
Patch0:		%{name}-PLD.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.8.1
BuildRequires:	gnome-common
BuildRequires:	gnome-vfs2-devel >= 2.12.0
BuildRequires:	intltool >= 0.31
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-filter
Provides:	xdg-menus
Obsoletes:	applnk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec .

%description -l pl
Pakiet zawiera implementacj� specyfikacji menu system�w biurkowych z
freedesktop.org: http://www.freedesktop.org/Standards/menu-spec .

%package editor
Summary:	Simple menu editor
Summary(pl):	Prosty edytor menu
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygtk-glade

%description editor
Simple menu editor.

%description editor -l pl
Prosty edytor menu.

%package filter-default
Summary:	Default gnome-menus filter
Summary(pl):	Domy�lny filtr gnome-menus
Group:		X11/Applications
Requires:	gnome-menus
Provides:	%{name}-filter
Obsoletes:	%{name}-filter-desktop

%description filter-default
Default gnome-menus filter. Includes all applications.

%description filter-default -l pl
Domy�lny filtr gnome-menus. Zawiera wszystkie aplikacje.

%package libs
Summary:	gnome-menus library
Summary(pl):	Biblioteka gnome-menus
Group:		Libraries
Provides:	gnome-vfs-menu-module = 1.1-1
Provides:	gnome-vfs2-module-menu = 1.1-1 
Obsoletes:	gnome-vfs-menu-module
Obsoletes:	gnome-vfs2-module-menu
Obsoletes:	gnome-vfs2-vfolder-menu

%description libs
gnome-menus library.

%description libs -l pl
Biblioteka gnome-menus.

%package devel
Summary:	Header files of gnome-menus library
Summary(pl):	Pliki nag��wkowe biblioteki gnome-menus
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.8.1

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
%patch0 -p1

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
rm -f $RPM_BUILD_ROOT%{py_sitedir}/GMenuSimpleEditor/*.{a,la,py}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{a,la}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-menu-spec-test
%{_datadir}/desktop-directories

%files editor
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gmenu-simple-editor
%{_datadir}/%{name}
%{_desktopdir}/gmenu-simple-editor.desktop
%dir %{py_sitedir}/GMenuSimpleEditor
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/GMenuSimpleEditor/*.py[co]

%files filter-default
%defattr(644,root,root,755)
%{_sysconfdir}/xdg/menus

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
