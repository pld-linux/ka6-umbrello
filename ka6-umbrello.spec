# Conditional build:
%bcond_with  apidocs           # build API docs

%define		kdeappsver	26.04.0
%define		kframever	6.22.0
%define		qtver		6.10.0
%define		kaname		umbrello
Summary:	Umbrello
Name:		ka6-%{kaname}
Version:	26.04.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	a97d076fbdf50edf14b31116e464de05
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	clang-devel >= 2.8.12
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-ktexteditor-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kf6-syntax-highlighting-devel >= %{kframever}
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%ifarch %{x8664}
BuildRequires:	ka6-kdevelop-devel >= 5.1.2
BuildRequires:	kf6-threadweaver-devel >= %{kframever}
%endif
Requires(post,postun):	desktop-file-utils
Requires:	%{name}-data = %{version}-%{release}
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Umbrello is a Unified Modelling Language (UML) modelling tool and code
generator. It can create diagrams of software and other systems in the
industry-standard UML format, and can also generate code from UML
diagrams in a variety of programming languages.

Features

- Supported formats: XMI
- Several type of diagrams supported: use case, class, sequence,
  collaboration, state, activity, component, deployment, entity
  relationship

%package apidocs
Summary:	Apidocs for %{kaname}
Summary(pl.UTF-8):	Dokumentacja API dla %{kaname}
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description apidocs
Apidocs for %{kaname}.

%description apidocs -l pl.UTF-8
Dokumentacja API dla %{kaname}.

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
Obsoletes:	ka5-%{kaname}-data < %{version}
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6 \
	%{!?with_apidocs:-DBUILD_APIDOC=OFF}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/po2xmi6
%attr(755,root,root) %{_bindir}/umbrello6
%attr(755,root,root) %{_bindir}/xmi2pot6

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_datadir}/umbrello6/apidoc
%{_docdir}/qt6-doc/umbrello.qch
%endif

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.umbrello.desktop
%{_iconsdir}/hicolor/*x*/apps/umbrello.png
%{_iconsdir}/hicolor/*x*/mimetypes/application-x-uml.png
%{_iconsdir}/hicolor/scalable/apps/umbrello.svgz
%{_datadir}/metainfo/org.kde.umbrello.appdata.xml
%{_datadir}/umbrello6
