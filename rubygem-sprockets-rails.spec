%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from sprockets-rails-2.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sprockets-rails

# Disable tests for this build due to broken rubygem-rack dep in rawhide
%global enable_test 1

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.0.0
Release: 3%{?dist}
Summary: Sprockets Rails integration
Group: Development/Languages
License: MIT
URL: https://github.com/rails/sprockets-rails
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# License file from the git repo
# https://github.com/rails/sprockets-rails/pull/75
Source1: LICENSE
# Get the tests
# git clone https://github.com/rails/sprockets-rails.git && cd sprockets-rails/
# git checkout v2.0.0
# tar czvf sprockets-rails-2.0.0-tests.tgz test/
Source2: sprockets-rails-%{version}-tests.tgz
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(sprockets) => 2.8
Requires: %{?scl_prefix}rubygem(sprockets) < 3
Requires: %{?scl_prefix}rubygem(actionpack) >= 3.0
Requires: %{?scl_prefix}rubygem(activesupport) >= 3.0
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
%if 0%{enable_test} > 0
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(sprockets)
BuildRequires: %{?scl_prefix}rubygem(railties)
BuildRequires: %{?scl_prefix_ruby}rubygem(rake)
%endif
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Provides Sprockets implementation for Rails 4.x (and beyond) Asset Pipeline.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %scl - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}
%setup -q -D -T -n  %{gem_name}-%{version}
%{?scl:scl enable %scl - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
%{?scl:scl enable %scl - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

# Move license into place
cp %{SOURCE1} .%{gem_instdir}/LICENSE

# Move the tests into place
tar xzvf %{SOURCE2} -C .%{gem_instdir}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%if 0%{enable_test} > 0
pushd ./%{gem_instdir}
# Running the test suite separately works fine
%{?scl:scl enable %scl - << \EOF}
testrb -Ilib test/test_helper.rb
testrb -Ilib test/test_task.rb
%{?scl:EOF}

# We need minitest 4.7.5. Disable for now.
# https://github.com/seattlerb/minitest/pull/275
#testrb -Ilib test/test_railtie.rb
popd
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/test

%changelog
* Thu Aug 08 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-3
- Enable tests

* Wed Jul 31 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-2
- Disable tests for now due to broken deps in Rails

* Mon Jul 22 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-1
- Initial package
