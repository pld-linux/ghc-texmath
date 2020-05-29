#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	texmath
Summary:	Conversion of LaTeX math formulas to MathML or OMML
Summary(pl.UTF-8):	Przekształcanie LaTeXowych wzorów matematycznych do MathML-a lub OMML-a
Name:		ghc-%{pkgname}
Version:	0.12.0.2
Release:	1
License:	GPL v2+
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/texmath
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	2dcb3994f890643d4bcecee90032e82f
URL:		http://hackage.haskell.org/package/texmath
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-aeson
BuildRequires:	ghc-base >= 4.8
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-containers
BuildRequires:	ghc-mtl
BuildRequires:	ghc-network-uri >= 2.6
BuildRequires:	ghc-pandoc-types >= 1.20
BuildRequires:	ghc-parsec >= 3
BuildRequires:	ghc-syb >= 0.4.2
BuildRequires:	ghc-text
BuildRequires:	ghc-xml
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-aeson-prof
BuildRequires:	ghc-base-prof >= 4.8
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-mtl-prof
BuildRequires:	ghc-network-uri-prof >= 2.6
BuildRequires:	ghc-pandoc-types-prof >= 1.20
BuildRequires:	ghc-parsec-prof >= 3
BuildRequires:	ghc-syb-prof >= 0.4.2
BuildRequires:	ghc-text-prof
BuildRequires:	ghc-xml-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-aeson
Requires:	ghc-base >= 4.8
Requires:	ghc-bytestring
Requires:	ghc-containers
Requires:	ghc-mtl
Requires:	ghc-network-uri >= 2.6
Requires:	ghc-pandoc-types >= 1.20
Requires:	ghc-parsec >= 3
Requires:	ghc-syb >= 0.4.2
Requires:	ghc-text
Requires:	ghc-xml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The texmathml library provides functions to convert LaTeX math
formulas to presentation MathML (which can be used in HTML) or OMML
(Office Math Markup Language, used in Microsoft Office). It supports
basic LaTeX and AMS extensions, and it can parse and apply LaTeX
macros.

%description -l pl.UTF-8
Biblioteka texmathml dostarcza funkcje do przekształcania LaTeXowych
wzorów matematycznych na prezentacyjne MathML (które można używać w
HTML-u) albo OMML (Office Math Markup Language, używane w Microsoft
Office). Obsługuje podstawowy LaTeX i rozszerzenia AMS, potrafi
analizować i wykonywać makra LaTeXa.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-prof >= 6.12.3
Requires:	ghc-aeson-prof
Requires:	ghc-base-prof >= 4.8
Requires:	ghc-bytestring-prof
Requires:	ghc-containers-prof
Requires:	ghc-mtl-prof
Requires:	ghc-network-uri-prof >= 2.6
Requires:	ghc-pandoc-types-prof >= 1.20
Requires:	ghc-parsec-prof >= 3
Requires:	ghc-syb-prof >= 0.4.2
Requires:	ghc-text-prof
Requires:	ghc-xml-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--flags="test executable" \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/texmath
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStexmath-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStexmath-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStexmath-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/MathML
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/MathML/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/MathML/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/TeX
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/TeX/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/TeX/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Unicode
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Unicode/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Unicode/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Writers
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Writers/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Writers/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStexmath-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/MathML/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Readers/TeX/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Unicode/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/Writers/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
