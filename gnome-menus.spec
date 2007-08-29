Summary:	Implementation of the draft Desktop Menu Specification
Summary(pl.UTF-8):	Implementacja specyfikacji menu systemów biurkowych
Name:		gnome-menus
Version:	2.19.90
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-menus/2.19/%{name}-%{version}.tar.bz2
# Source0-md5:	69b746d6776269882ff05c2f20e32390
Patch0:		%{name}-PLD.patch
Patch1:		%{name}-nokde.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	fam-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.14.0
BuildRequires:	gnome-common
BuildRequires:	intltool >= 0.36.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2.2
BuildRequires:	rpm-pythonprov
Requires:	%{name}-filter
Requires:	%{name}-libs = %{version}-%{release}
Provides:	xdg-menus
Conflicts:	applnk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec .

%description -l pl.UTF-8
Pakiet zawiera implementację specyfikacji menu systemów biurkowych z
freedesktop.org: http://www.freedesktop.org/Standards/menu-spec .

%package editor
Summary:	Simple menu editor
Summary(pl.UTF-8):	Prosty edytor menu
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygtk-glade >= 2:2.10.4

%description editor
Simple menu editor.

%description editor -l pl.UTF-8
Prosty edytor menu.

%package filter-default
Summary:	Default gnome-menus filter
Summary(pl.UTF-8):	Domyślny filtr gnome-menus
Group:		X11/Applications
Requires:	gnome-menus
Provides:	%{name}-filter
Obsoletes:	gnome-menus-filter-desktop

%description filter-default
Default gnome-menus filter. Includes all applications.

%description filter-default -l pl.UTF-8
Domyślny filtr gnome-menus. Zawiera wszystkie aplikacje.

%package libs
Summary:	gnome-menus library
Summary(pl.UTF-8):	Biblioteka gnome-menus
Group:		Libraries
Provides:	gnome-vfs-menu-module = 1.1-1
Provides:	gnome-vfs2-module-menu = 1.1-1
Obsoletes:	gnome-vfs-menu-module
Obsoletes:	gnome-vfs2-module-menu
Obsoletes:	gnome-vfs2-vfolder-menu

%description libs
gnome-menus library.

%description libs -l pl.UTF-8
Biblioteka gnome-menus.

%package devel
Summary:	Header files of gnome-menus library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gnome-menus
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	fam-devel
Requires:	glib2-devel >= 1:2.14.0

%description devel
Headers for gnome-menus library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gnome-menus.

%package static
Summary:	Static gnome-menus library
Summary(pl.UTF-8):	Statyczna biblioteka gnome-menus
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of gnome-menu library.

%description static -l pl.UTF-8
Statyczna biblioteka gnome-menu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-static \
	--enable-python
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/gn
rm -f $RPM_BUILD_ROOT%{py_sitedir}/GMenuSimpleEditor/*.{a,la,py}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/*.{a,la}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/applications-merged

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
