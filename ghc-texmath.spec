#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	texmath
Summary:	Conversion of LaTeX math formulas to MathML or OMML
Summary(pl.UTF-8):	Przekształcanie LaTeXowych wzorów matematycznych do MathML-a lub OMML-a
Name:		ghc-%{pkgname}
Version:	0.6.5.2
Release:	1
License:	GPL v2+
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/texmath
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	4ce0eac8bc24742f43c8f71231565803
URL:		http://hackage.haskell.org/package/texmath
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-containers
BuildRequires:	ghc-pandoc-types
BuildRequires:	ghc-parsec >= 3
BuildRequires:	ghc-syb
BuildRequires:	ghc-xml
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-pandoc-types-prof
BuildRequires:	ghc-parsec-prof >= 3
BuildRequires:	ghc-syb-prof
BuildRequires:	ghc-xml-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-containers
Requires:	ghc-pandoc-types
Requires:	ghc-parsec >= 3
Requires:	ghc-syb
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
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-containers-prof
Requires:	ghc-pandoc-types-prof
Requires:	ghc-parsec-prof >= 3
Requires:	ghc-syb-prof
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
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--flags="test" \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{pkgname}-%{version}/tests

runhaskell Setup.hs register \
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
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HStexmath-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStexmath-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHStexmath-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/TeXMath/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
