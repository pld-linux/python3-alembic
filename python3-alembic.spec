#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Database migration tool for SQLAlchemy
Summary(pl.UTF-8):	Narzędzie do migracji baz danych dla SQLAlchemy
Name:		python3-alembic
Version:	1.17.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/alembic/
Source0:	https://files.pythonhosted.org/packages/source/a/alembic/alembic-%{version}.tar.gz
# Source0-md5:	a273b94a21e8a0809a5b3f06b6eb14cf
URL:		https://pypi.org/project/alembic/
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools >= 1:77.0.3
%if %{with tests}
BuildRequires:	python3-Mako
BuildRequires:	python3-black >= 25.1
BuildRequires:	python3-editor >= 0.3
BuildRequires:	python3-pytest >= 8.1
BuildRequires:	python3-sqlalchemy >= 1.3.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
#BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Alembic is a database migrations tool written by the author of
SQLAlchemy. A migrations tool offers the following functionality:
- Can emit ALTER statements to a database in order to change the
  structure of tables and other constructs.
- Provides a system whereby "migration scripts" may be constructed;
  each script indicates a particular series of steps that can
  "upgrade" a target database to a new version, and optionally a
  series of steps that can "downgrade" similarly, doing the same steps
  in reverse.
- Allows the scripts to execute in some sequential manner.

%description -l pl.UTF-8
Alembic to narzędzie do migracji baz danych, napisane przez autora
SQLAlchemy. Narzędzie oferuje następującą funkcjonalność:
- może tworzyć instrukcje ALTER do zmiany struktury tabel i innych
  elementów bazy danych;
- zapewnia system tworzenia "skryptów migracyjnych", gdzie każdy
  skrypt określa konkretną sekwencję kroków do "uaktualnienia"
  docelowej bazy do nowej wersji oraz opcjonalnie analogiczną
  sekwencję kroków do "cofnięcia" bazy;
- pozwala na wykonywanie skryptów w pewien sekwencyjny sposób.

%package apidocs
Summary:	API documentation for Python alembic module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona alembic
Group:		Documentation

%description apidocs
API documentation for Python alembic module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona alembic.

%prep
%setup -q -n alembic-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

# sdist contains prebuilt doc, no need to regenerate currently
%if 0 && %{with doc}
%{__make} -C docs/build html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/alembic{,-3}
ln -sf alembic-3 $RPM_BUILD_ROOT%{_bindir}/alembic

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README.rst
%attr(755,root,root) %{_bindir}/alembic
%attr(755,root,root) %{_bindir}/alembic-3
%{py3_sitescriptdir}/alembic
%{py3_sitescriptdir}/alembic-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/{_images,_static,api,*.html,*.js}
%endif
