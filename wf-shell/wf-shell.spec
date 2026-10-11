%global forgeurl https://github.com/WayfireWM/wf-shell
# 'libgnome-volume-control'
# This project is only intended to be used as a subproject
%global gvc_commit      0a4eda0cdc2deb352bebc70ec697c42af46094e4
%global gvc_shortcommit %(c=%{gvc_commit}; echo ${c:0:7})

#   * wf-json
%global commit2 70039e13cdeaebd8ec498ed30bf5ab91c2e313ec
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})

Name:           wf-shell
Version:        0.11.0
%forgemeta
Release:        %autorelease
Summary:        A GTK4-based panel for wayfire

License:        MIT
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        https://github.com/GNOME/libgnome-volume-control/tarball/%{gvc_commit}#/gvc-%{gvc_shortcommit}.tar.gz
Source2:        https://github.com/WayfireWM/wf-json/archive/%{commit2}/wf-json-%{shortcommit2}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  glm-devel
BuildRequires:  meson >= 0.51.0
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gtk4-layer-shell-0) >= 1.3.0
BuildRequires:  pkgconfig(gtkmm-4.0) >= 4.12
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(wireplumber-0.5)
BuildRequires:  pkgconfig(dbusmenu-glib-0.4)
BuildRequires:  pkgconfig(wayfire)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wf-config) >= 0.11.0
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(ddcutil)
BuildRequires:  pkgconfig(openssl)

Recommends:     wayland-logout

Requires:       hicolor-icon-theme

Provides:       bundled(gvc) = 0.git%{gvc_shortcommit}
Provides:       bundled(wf-json) = 0.0~git%{commit2}

%description
A collection of GTK4-based desktop components designed for Wayfire and Wlroots desktops

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.


%prep
%forgeautosetup -p1
%autosetup -D -T -a1
%autosetup -D -T -a2
mv GNOME-libgnome-volume-control-%{gvc_shortcommit}/* \
    %{_builddir}/%{name}-%{version}/subprojects/gvc
mv wf-json-%{commit2}/* subprojects/wf-json/

%build
%meson \
    -Dwayland-logout=false
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md %{name}.ini.example
%{_datadir}/%{name}/
%{_sysconfdir}/pam.d/wf-locker
%{_sysconfdir}/xdg/xdg-desktop-portal-wlr/wayfire
%{_bindir}/wf-background
%{_bindir}/wf-dock
%{_bindir}/wf-panel
%{_bindir}/wf-locker
%{_bindir}/wf-locker-pin
%{_bindir}/wf-stream-chooser
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/applications/*.desktop

%files devel
%{_libdir}/pkgconfig/*.pc


%changelog
%autochangelog
