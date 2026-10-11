%global forgeurl https://github.com/WayfireWM/wayfire

# Git submodules
#   * wf-utils
%global commit1 329c3ff01724d82947f61c45332f75d3534e8454
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

#   * wf-touch
%global commit2 d7ae5e7fa4de9536e2de2af74f168f981eb8a77a
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})

#   * wf-json
%global commit3 70039e13cdeaebd8ec498ed30bf5ab91c2e313ec
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})

Name:           wayfire
Version:        0.11.0
%forgemeta
Release:        %autorelease
Summary:        A modular and extensible wayland compositor

License:        MIT
URL:            https://wayfire.org
Source0:        %{forgesource}
Source1:        https://github.com/WayfireWM/wf-utils/archive/%{commit1}/wf-utils-%{shortcommit1}.tar.gz
Source2:        https://github.com/WayfireWM/wf-touch/archive/%{commit2}/wf-touch-%{shortcommit2}.tar.gz
Source3:        https://github.com/WayfireWM/wf-json/archive/%{commit3}/wf-json-%{shortcommit3}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  inotify-tools-devel
BuildRequires:  libevdev-devel
BuildRequires:  meson >= 0.64.0

BuildRequires:  cmake(doctest)
BuildRequires:  cmake(glm)

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput) >= 1.7.0
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(nlohmann_json) >= 3.11.2
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(yyjson)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.37
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wf-config) >= 0.11.0
BuildRequires:  pkgconfig(wlroots-0.20)
BuildRequires:  pkgconfig(xkbcommon)

Recommends:     wayfire-config-manager
Recommends:     wf-shell

Provides:       bundled(wf-utils) = 0.0~git%{commit1}
Provides:       bundled(wf-touch) = 0.0~git%{commit2}
Provides:       bundled(wf-json) = 0.0~git%{commit3}


%description
Wayfire is a 3D Wayland compositor, inspired by Compiz and based on wlroots.

It aims to create a customizable, extendable and lightweight environment without
sacrificing its appearance.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.


%prep
%forgeautosetup -p1
%autosetup -D -T -a1
%autosetup -D -T -a2
%autosetup -D -T -a3
mv wf-utils-%{commit1}/* subprojects/wf-utils/
mv wf-touch-%{commit2}/* subprojects/wf-touch/
mv wf-json-%{commit3}/* subprojects/wf-json/



%build
%meson                            \
    -Duse_system_wfconfig=enabled \
    -Duse_system_wlroots=enabled  \
    -Dxwayland=enabled            \
    %{nil}
%meson_build


%install
%meson_install
install -D -p -m 0644 %{name}.desktop %{buildroot}%{_datadir}/wayland-sessions/%{name}.desktop
rm -f %{buildroot}%{_libdir}/libwftouch.a
# Duplicate man file
rm -f %{buildroot}%{_prefix}/man/%{name}.1


%files
%license LICENSE
%doc README.md %{name}.ini
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/wayland-sessions/*.desktop
%{_datadir}/xdg-desktop-portal/wayfire-portals.conf
%{_libdir}/%{name}/
%{_libdir}/lib%{name}-blur-base.so
%{_libdir}/libwf-utils.so.0*
%{_mandir}/man1/*.1*
%{_datadir}/locale/*/*/*.mo
%{_bindir}/wayfire-plugin

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}-*.a
%{_libdir}/libwf-utils.so
%{_libdir}/pkgconfig/*.pc


%changelog
%autochangelog
