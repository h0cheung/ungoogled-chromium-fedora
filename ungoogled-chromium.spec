%global debug_package %{nil}
#Global Libraries
%global menu_name Ungoogled Chromium
%global xdg_subdir ungoogled-chromium
%ifarch aarch64
%global _smp_build_ncpus 6
%endif
%undefine _auto_set_build_flags
#This can be any folder on out
%global target out/Release
### Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
### Note: These are for Fedora use ONLY.
### For your own distribution, please get your own set of keys.
### http://lists.debian.org/debian-legal/2013/11/msg00006.html
%global api_key AIzaSyDUIXvzVrt5OkVsgXhQ6NFfvWlA44by-aw
###############################Exclude Private chromium libs###########################
%global __requires_exclude %{chromiumdir}/.*\\.so
%global __provides_exclude_from %{chromiumdir}/.*\\.so
#######################################CONFIGS###########################################
# System libraries to use.
%global system_libdrm 0
# Chrome upstream uses custom ffmpeg patches
%global system_ffmpeg 0
%global system_flac 0
%global system_fontconfig 0
# fedora freetype is too old
%global system_freetype 0
%global system_harfbuzz 0
%global system_libjpeg 0
%global system_libicu 0
# lto issue with system libpng
%global system_libpng 0
%global system_libvpx 0
# The libxml_utils code depends on the specific bundled libxml checkout
%global system_libxml2 0
# lto issue with system minizip
%global system_minizip 0
%global system_re2 0
%global system_libwebp 0
%global system_xslt 0
%global system_snappy 0

##############################Package Definitions######################################
Name:           ungoogled-chromium
Version:        102.0.5005.61
Release:        2%{?dist}
Summary:        Chromium built with all freeworld codecs and VA-API support
License:        BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:            https://github.com/Eloston/ungoogled-chromium
Source0:        https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz

# Patchset composed by Stephan Hartmann.
%global patchset_revision chromium-102-patchset-6
Source1:        https://github.com/stha09/chromium-patches/archive/%{patchset_revision}/chromium-patches-%{patchset_revision}.tar.gz

# The following two source files are copied and modified from the chromium source
Source10:       %{name}.sh
#Add our own appdata file.
Source11:       %{name}.appdata.xml
Source12:       chromium-symbolic.svg
#Personal stuff
Source15:       LICENSE

%global ungoogled_chromium_revision %{version}-3
Source300:      https://github.com/Eloston/ungoogled-chromium/archive/%{ungoogled_chromium_revision}/ungoogled-chromium-%{ungoogled_chromium_revision}.tar.gz
######################## Installation Folder #################################################
#Our installation folder
%global chromiumdir %{_libdir}/%{name}
########################################################################################
BuildRequires:  util-linux
BuildRequires:  clang, clang-tools-extra
BuildRequires:  lld
BuildRequires:  llvm
# Basic tools and libraries needed for building
BuildRequires:  ninja-build, nodejs, bison, gperf, hwdata
BuildRequires:  libatomic, flex, perl-Switch, elfutils, git-core
BuildRequires:  libcap-devel, cups-devel, alsa-lib-devel
BuildRequires:  mesa-libGL-devel, mesa-libEGL-devel
# Pipewire need this.
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libexif), pkgconfig(nss)
BuildRequires:  pkgconfig(xtst), pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(dbus-1), pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(libudev), pkgconfig(uuid)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xcb-proto)
BuildRequires:  pkgconfig(gnome-keyring-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  expat-devel
BuildRequires:  pciutils-devel
BuildRequires:  speech-dispatcher-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libcurl-devel
BuildRequires:  libxshmfence-devel
# install desktop files
BuildRequires:  desktop-file-utils
# install AppData files
BuildRequires:  libappstream-glib
# Libstdc++ static needed for linker
BuildRequires:  libstdc++-static
#for vaapi
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)

BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command
BuildRequires:  python3-beautifulsoup4
BuildRequires:  python3-html5lib
BuildRequires:  python3-json5
BuildRequires:  python3-mako
BuildRequires:  python3-markupsafe
BuildRequires:  python3-ply
BuildRequires:  python3-simplejson
BuildRequires:  python3-six
# replace_gn_files.py --system-libraries
%if %{system_flac}
BuildRequires:  flac-devel
%endif
%if %{system_freetype}
BuildRequires:  freetype-devel
%endif
%if %{system_harfbuzz}
BuildRequires:  harfbuzz-devel
%endif
%if %{system_libicu}
BuildRequires:  libicu-devel
%endif
%if %{system_libjpeg}
BuildRequires:  libjpeg-turbo-devel
%endif
%if %{system_libpng}
BuildRequires:  libpng-devel
%endif
%if %{system_libvpx}
BuildRequires:  libvpx-devel
%endif
%if %{system_ffmpeg}
BuildRequires:  ffmpeg-devel
BuildRequires:  opus-devel
%endif
%if %{system_libwebp}
BuildRequires:  libwebp-devel
%endif
%if %{system_minizip}
BuildRequires:  minizip-compat-devel
%endif
%if %{system_libxml2}
BuildRequires:  pkgconfig(libxml-2.0)
%endif
%if %{system_xslt}
BuildRequires:  pkgconfig(libxslt)
%endif
%if %{system_re2}
BuildRequires:  re2-devel
%endif
%if %{system_snappy}
BuildRequires:  snappy-devel
%endif

# Runtime Requirements
Requires:       hicolor-icon-theme
# GTK modules it expects to find for some reason.
Requires:       libcanberra-gtk3%{_isa}
#Some recommendations
Recommends:     libva-utils

# This build should be only available to amd64
ExclusiveArch:  x86_64 %{arm64}

# Gentoo patches:
Patch201:       chromium-98-EnumTable-crash.patch
Patch202:       chromium-InkDropHost-crash.patch

# Arch Linux patches:
Patch227:       remove-no-opaque-pointers-flag.patch
Patch1228:      add-a-TODO-about-a-missing-pnacl-flag.patch
Patch1229:      use-ffile-compilation-dir.patch

# Suse patches:
Patch232:       chromium-91-sql-standard-layout-type.patch
Patch233:       chromium-clang-nomerge.patch

# Fedora patches:
Patch300:       chromium-py3-bootstrap.patch
Patch301:       chromium-gcc11.patch
Patch302:       chromium-java-only-allowed-in-android-builds.patch
Patch303:       chromium-aarch64-cxxflags-addition.patch

# RPM Fusion patches [free/chromium-freeworld]:
Patch401:       chromium-fix-vaapi-on-intel.patch
Patch402:       chromium-enable-widevine.patch
Patch403:       chromium-manpage.patch
Patch404:       chromium-md5-based-build-id.patch
Patch405:       chromium-names.patch
Patch406:       gcc12.patch
Patch407:       allow-to-override-clang-through-env-variables.patch

%description
ungoogled-chromium is Chromium, sans integration with Google. It also features
some tweaks to enhance privacy, control, and transparency (almost all of which
require manual activation or enabling).

ungoogled-chromium retains the default Chromium experience as closely as
possible. Unlike other Chromium forks that have their own visions of a web
browser, ungoogled-chromium is essentially a drop-in replacement for Chromium.
############################################PREP###########################################################
%prep
%setup -q -T -n chromium-patches-%{patchset_revision} -b 1
%setup -q -T -n ungoogled-chromium-%{ungoogled_chromium_revision} -b 300
%setup -q -n chromium-%{version}

%global patchset_root %{_builddir}/chromium-patches-%{patchset_revision}
%global ungoogled_chromium_root %{_builddir}/ungoogled-chromium-%{ungoogled_chromium_revision}

# Apply patchset composed by Stephan Hartmann.
%global patchset_apply() \
  printf "Applying %%s\\n" %{1} \
  %{__scm_apply_patch -p1} <%{patchset_root}/%{1}

%patchset_apply chromium-78-protobuf-RepeatedPtrField-export.patch
%patchset_apply chromium-102-fenced_frame_utils-include.patch
%patchset_apply chromium-102-regex_pattern-array.patch
%patchset_apply chromium-102-swiftshader-template-instantiation.patch

# ungoogled-chromium: binary pruning.
python3 -B %{ungoogled_chromium_root}/utils/prune_binaries.py . \
  %{ungoogled_chromium_root}/pruning.list

# Apply patches up to #1000 from this spec.
%autopatch -M1000 -p1

# Manually apply patches that need an ifdef
%if 0%{?fedora} < 35
%patch1228 -Rp1
%patch1229 -Rp1
%endif

./build/linux/unbundle/replace_gn_files.py --system-libraries \
%if %{system_ffmpeg}
    ffmpeg \
    opus \
%endif
%if %{system_harfbuzz}
    harfbuzz-ng \
%endif
%if %{system_flac}
    flac \
%endif
%if %{system_freetype}
    freetype \
%endif
%if %{system_fontconfig}
    fontconfig \
%endif
%if %{system_libicu}
    icu \
%endif
%if %{system_libdrm}
    libdrm \
%endif
%if %{system_libjpeg}
    libjpeg \
%endif
%if %{system_libpng}
    libpng \
%endif
%if %{system_libvpx}
    libvpx \
%endif
%if %{system_libwebp}
    libwebp \
%endif
%if %{system_libxml2}
    libxml \
%endif
%if %{system_xslt}
    libxslt \
%endif
%if %{system_re2}
    re2 \
%endif
%if %{system_snappy}
    snappy \
%endif
%if %{system_minizip}
    zlib
%endif

# Too much debuginfo
sed -i 's|-g2|-g0|g' build/config/compiler/BUILD.gn

sed -i 's|//third_party/usb_ids|/usr/share/hwdata|g' \
    services/device/public/cpp/usb/BUILD.gn

sed -i \
	-e 's/"-ffile-compilation-dir=."//g' \
	-e 's/"-no-canonical-prefixes"//g' \
	build/config/compiler/BUILD.gn

mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node

mkdir -p buildtools/third_party/eu-strip/bin
ln -sf %{_bindir}/eu-strip buildtools/third_party/eu-strip/bin/eu-strip

rm -f -- third_party/depot_tools/ninja
ln -s %{_bindir}/ninja third_party/depot_tools/ninja
ln -s %{_bindir}/python3 third_party/depot_tools/python

# ungoogled-chromium: patches
python3 -B %{ungoogled_chromium_root}/utils/patches.py apply . \
  %{ungoogled_chromium_root}/patches

# ungoogled-chromium: domain substitution
%if %{with domain_substitution}
rm -f %{_builddir}/dsc.tar.gz
python3 -B %{ungoogled_chromium_root}/utils/domain_substitution.py apply . \
  -r %{ungoogled_chromium_root}/domain_regex.list \
  -f %{ungoogled_chromium_root}/domain_substitution.list \
  -c %{_builddir}/dsc.tar.gz
%endif

%build
# Final link uses lots of file descriptors.
ulimit -n 2048

#export compilar variables
export CC="clang"
export CXX="clang++"
export AR="llvm-ar"
export NM="llvm-nm"
export READELF="llvm-readelf"

export RANLIB="ranlib"
export PATH="$PWD/third_party/depot_tools:$PATH"
export CHROMIUM_RPATH="%{_libdir}/%{name}"

FLAGS='-Wno-unknown-warning-option'
export CFLAGS="$FLAGS"
export CXXFLAGS="$FLAGS"

CHROMIUM_GN_DEFINES=
gn_arg() { CHROMIUM_GN_DEFINES="$CHROMIUM_GN_DEFINES $*"; }

gn_arg 'rpm_fusion_package_name="%{name}"'
gn_arg 'rpm_fusion_menu_name="%{menu_name}"'
gn_arg custom_toolchain=\"//build/toolchain/linux/unbundle:default\"
gn_arg host_toolchain=\"//build/toolchain/linux/unbundle:default\"
gn_arg is_official_build=true
gn_arg disable_fieldtrial_testing_config=true
gn_arg use_custom_libcxx=false
gn_arg use_sysroot=false
gn_arg use_gio=true
gn_arg use_glib=true
gn_arg use_libpci=true
gn_arg use_pulseaudio=true
gn_arg use_aura=true
gn_arg use_cups=true
gn_arg use_kerberos=true
gn_arg use_gold=false
gn_arg use_vaapi=true
gn_arg optimize_webui=false
%if %{system_freetype}
gn_arg use_system_freetype=true
%endif
%if %{system_harfbuzz}
gn_arg use_system_harfbuzz=true
%endif
gn_arg link_pulseaudio=true
gn_arg enable_hangout_services_extension=false
gn_arg treat_warnings_as_errors=false
gn_arg fatal_linker_warnings=false
gn_arg system_libdir=\"%{_lib}\"
gn_arg use_allocator=\"none\"
gn_arg use_icf=false
gn_arg enable_js_type_check=false
gn_arg use_system_libwayland=true
gn_arg use_system_wayland_scanner=true
gn_arg use_bundled_weston=false

# ffmpeg
gn_arg ffmpeg_branding=\"Chrome\"
gn_arg proprietary_codecs=true

# Remove debug
gn_arg is_debug=false
gn_arg symbol_level=0

gn_arg enable_nacl=false
gn_arg is_component_build=false
gn_arg enable_widevine=true

gn_arg rtc_use_pipewire=true
gn_arg rtc_link_pipewire=true

gn_arg clang_base_path=\"%{_prefix}\"
gn_arg is_clang=true
gn_arg clang_use_chrome_plugins=false
gn_arg use_lld=true
%ifarch %{arm64}
gn_arg 'target_cpu="arm64"'
gn_arg use_thin_lto=false
%else
gn_arg use_thin_lto=true
%endif
gn_arg is_cfi=false
gn_arg use_cfi_icall=false
gn_arg chrome_pgo_phase=0

%if %{system_libicu}
gn_arg icu_use_data_file=false
%endif

gn_arg enable_vulkan=true

gn_arg 'google_api_key="%{api_key}"'

# ungoogled
gn_arg build_with_tflite_lib=false
gn_arg chrome_pgo_phase=0
gn_arg clang_use_chrome_plugins=false
gn_arg disable_fieldtrial_testing_config=true
gn_arg enable_hangout_services_extension=false
gn_arg enable_js_type_check=false
gn_arg enable_mdns=false
gn_arg enable_mse_mpeg2ts_stream_parser=true
gn_arg enable_nacl=false
gn_arg enable_one_click_signin=false
gn_arg enable_reading_list=false
gn_arg enable_remoting=false
gn_arg enable_reporting=false
gn_arg enable_service_discovery=false
gn_arg enable_widevine=true
gn_arg exclude_unwind_tables=true
gn_arg 'google_api_key=""'
gn_arg 'google_default_client_id=""'
gn_arg 'google_default_client_secret=""'
gn_arg safe_browsing_mode=0
gn_arg treat_warnings_as_errors=false
gn_arg use_official_google_api_keys=false
gn_arg use_unofficial_version_number=false

tools/gn/bootstrap/bootstrap.py --gn-gen-args="$CHROMIUM_GN_DEFINES" --build-path=%{target}
%{target}/gn --script-executable=%{__python3} gen --args="$CHROMIUM_GN_DEFINES" %{target}
%ninja_build -C %{target} chrome chrome_sandbox

######################################Install####################################
%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromiumdir}/locales
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_metainfodir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps
sed -e "s|@@CHROMIUMDIR@@|%{chromiumdir}|"     %{SOURCE10} > %{name}.sh
install -m 755 %{name}.sh %{buildroot}%{_bindir}/%{name}
install -m 644 %{SOURCE11} %{buildroot}%{_metainfodir}
sed \
  -e "s|@@MENUNAME@@|Chromium|g" \
  -e "s|@@PACKAGE@@|%{name}|g" \
  -e "s|@@SUMMARY@@|%{summary}|g" \
  -e "s|@@XDG_SUBDIR@@|%{xdg_subdir}|g" \
  chrome/app/resources/manpage.1.in >chrome.1
install -m 644 chrome.1 %{buildroot}%{_mandir}/man1/%{name}.1
sed \
  -e "s|@@MENUNAME@@|%{menu_name}|g" \
  -e "s|@@PACKAGE@@|%{name}|g" \
  -e "s|%{_bindir}/@@USR_BIN_SYMLINK_NAME@@|%{name}|g" \
  chrome/installer/linux/common/desktop.template >%{name}.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{name}.desktop
sed \
  -e "s|@@INSTALLDIR@@|%{_bindir}|g" \
  -e "s|@@MENUNAME@@|%{menu_name}|g" \
  -e "s|@@PACKAGE@@|%{name}|g" \
  chrome/installer/linux/common/default-app.template >%{name}.xml
install -m 644 %{name}.xml %{buildroot}%{_datadir}/gnome-control-center/default-apps/
install -m 755 %{target}/chrome %{buildroot}%{chromiumdir}/%{name}
install -m 4755 %{target}/chrome_sandbox %{buildroot}%{chromiumdir}/chrome-sandbox
install -m 755 %{target}/chrome_crashpad_handler %{buildroot}%{chromiumdir}/
install -m 755 %{target}/libEGL.so %{buildroot}%{chromiumdir}/
install -m 755 %{target}/libGLESv2.so %{buildroot}%{chromiumdir}/
%if !%{system_libicu}
install -m 644 %{target}/icudtl.dat %{buildroot}%{chromiumdir}/
%endif
install -m 644 %{target}/v8_context_snapshot.bin %{buildroot}%{chromiumdir}/
install -m 644 %{target}/snapshot_blob.bin %{buildroot}%{chromiumdir}/
install -m 644 %{target}/*.pak %{buildroot}%{chromiumdir}/
install -m 644 %{target}/locales/*.pak %{buildroot}%{chromiumdir}/locales/
install -m 755 %{target}/xdg*  %{buildroot}%{chromiumdir}/
install -m 755 %{target}/libvk_swiftshader.so %{buildroot}%{chromiumdir}/
install -m 755 %{target}/libvulkan.so.1 %{buildroot}%{chromiumdir}/
install -m 644 %{target}/vk_swiftshader_icd.json %{buildroot}%{chromiumdir}/

# Icons
for i in 16 32; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/default_100_percent/chromium/product_logo_$i.png \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done
for i in 24 32 48 64 128 256; do
    if [ ${i} = 32 ]; then ext=xpm; else ext=png; fi
    if [ ${i} = 32 ]; then dir=linux/; else dir=; fi
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/chromium/${dir}product_logo_$i.${ext} \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.${ext}
done
install -m 644 %{SOURCE12} \
  %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/%{name}-symbolic.svg

strip %{buildroot}%{chromiumdir}/%{name}
strip %{buildroot}%{chromiumdir}/chrome-sandbox
strip %{buildroot}%{chromiumdir}/chrome_crashpad_handler
strip %{buildroot}%{chromiumdir}/libEGL.so
strip %{buildroot}%{chromiumdir}/libGLESv2.so
strip %{buildroot}%{chromiumdir}/libvk_swiftshader.so
strip %{buildroot}%{chromiumdir}/libvulkan.so.1

####################################check##################################################
%check
appstream-util validate-relax --nonet "%{buildroot}%{_metainfodir}/%{name}.appdata.xml"
######################################files################################################
%files
%license LICENSE
%doc AUTHORS
%{_bindir}/%{name}
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome-control-center/default-apps/%{name}.xml
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.xpm
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/symbolic/apps/%{name}-symbolic.svg
%{_mandir}/man1/%{name}.1.*
%dir %{chromiumdir}
%{chromiumdir}/%{name}
%{chromiumdir}/chrome-sandbox
%{chromiumdir}/chrome_crashpad_handler
%{chromiumdir}/libEGL.so
%{chromiumdir}/libGLESv2.so
%if !%{system_libicu}
%{chromiumdir}/icudtl.dat
%endif
%{chromiumdir}/v8_context_snapshot.bin
%{chromiumdir}/snapshot_blob.bin
%{chromiumdir}/*.pak
%{chromiumdir}/xdg-mime
%{chromiumdir}/xdg-settings
%dir %{chromiumdir}/locales
%{chromiumdir}/locales/*.pak
%{chromiumdir}/libvk_swiftshader.so
%{chromiumdir}/libvulkan.so.1
%{chromiumdir}/vk_swiftshader_icd.json
#########################################changelogs#################################################
%changelog
* Thu May 26 2022 Leigh Scott <leigh123linux@gmail.com> - 102.0.5005.61-1
- Initial reborn ungoogled build
