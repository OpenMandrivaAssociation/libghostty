%define libname %mklibname ghostty-vt
%define devname %mklibname ghostty-vt -d

Name:		%{libname}
# 1.4.0 was built from the Ghostty application tarball. libghostty-vt 1.0
# is the library's own first stable release, and that version sorts older.
Epoch:		1
Version:	1.0.0
Release:	1
Summary:	Ghostty terminal emulation library
Url:		https://lib.ghostty.org/vt/
# libghostty-vt: MIT
# highway: Apache-2.0 OR BSD-3-Clause
# simdutf, wuffs: Apache-2.0 OR MIT
# uucode: MIT AND Unicode-3.0
# translate-c: MIT
License:	MIT AND (Apache-2.0 OR BSD-3-Clause) AND (Apache-2.0 OR MIT) AND (MIT AND Unicode-3.0)
Group:		System/Libraries
Source0:	https://release.files.ghostty.org/libghostty-vt/%{version}/libghostty-vt-%{version}.tar.gz
# Unpacked Zig packages for an offline build. zig --system reads this directory.
Source1:	https://release.files.ghostty.org/libghostty-vt/%{version}/libghostty-vt-%{version}-deps.tar.gz
# zig 0.17 ships a broken amxtf32intrin.h, and on aarch64 its arm_neon.h
# declares bf16 builtins that do not exist. The patch skips the x86 header
# and disables Highway's NEON_BF16 target. Baseline NEON stays on.
Patch0:		libghostty-vt-%{version}-zig-amx-tf32.patch
BuildRequires:	zig >= 0.17.0
BuildRequires:	zig < 0.18

%description
Shared terminal emulation library from Ghostty, with a stable C ABI.
KDE terminal applications and other programs link this library. The
Ghostty GTK application is not included.

%package -n %{devname}
Summary:	Development files for %{libname}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Header files, pkg-config metadata, and the CMake package for %{libname}.

%prep
%autosetup -p1 -n libghostty-vt-%{version} -a 1
cp -a LICENSE LICENSE.ghostty
cp -a libghostty-vt-%{version}-deps/N-V-__8AAGmZhABbsPJLfbqrh6JTHsXhY6qCaLAQyx25e0XE/LICENSE LICENSE.highway
cp -a libghostty-vt-%{version}-deps/N-V-__8AAGmZhABbsPJLfbqrh6JTHsXhY6qCaLAQyx25e0XE/LICENSE-BSD3 LICENSE.highway-bsd3
cp -a libghostty-vt-%{version}-deps/N-V-__8AAP5JWgCGP_AD0teWpa4krRvE9VPZzvviGdbmN4jI/LICENSE-APACHE LICENSE.wuffs-apache
cp -a libghostty-vt-%{version}-deps/N-V-__8AAP5JWgCGP_AD0teWpa4krRvE9VPZzvviGdbmN4jI/LICENSE-MIT LICENSE.wuffs-mit
cp -a libghostty-vt-%{version}-deps/uucode-0.2.0-ZZjBPm6FVgBcY-79AHV8ckQj86z0JwOyVyj89VeZrEiv/LICENSE.md LICENSE.uucode
cp -a libghostty-vt-%{version}-deps/translate_c-2.0.0-Q_BUWltOBwBYABF84EUL208pIFeUIwbBs29FmVBaafN5/LICENSE LICENSE.translate-c
cp -a pkg/simdutf/vendor/LICENSE-APACHE LICENSE.simdutf-apache
cp -a pkg/simdutf/vendor/LICENSE-MIT LICENSE.simdutf-mit

%install
# SIMD stays on. The 1.0 packaging notes say a general-purpose package
# should keep the bundled simdutf and highway paths.
# An empty global cache makes Zig use only the --system packages.
DESTDIR="%{buildroot}" \
ZIG_GLOBAL_CACHE_DIR="%{_builddir}/zig-global-cache" \
zig build \
	--cache-dir "%{_builddir}/zig-local-cache" \
	--system "%{_builddir}/libghostty-vt-%{version}/libghostty-vt-%{version}-deps" \
	--build-id=sha1 \
	-Doptimize=ReleaseFast \
	-Dcpu=baseline \
	--prefix %{_prefix} \
	--prefix-lib-dir %{_lib}
rm -f %{buildroot}%{_libdir}/libghostty-vt.a \
	%{buildroot}%{_libdir}/pkgconfig/libghostty-vt-static.pc

%files
%license LICENSE.ghostty
%license LICENSE.highway
%license LICENSE.highway-bsd3
%license LICENSE.wuffs-apache
%license LICENSE.wuffs-mit
%license LICENSE.uucode
%license LICENSE.translate-c
%license LICENSE.simdutf-apache
%license LICENSE.simdutf-mit
%{_libdir}/libghostty-vt.so.1*

%files -n %{devname}
%{_includedir}/ghostty
%{_libdir}/libghostty-vt.so
%{_libdir}/pkgconfig/libghostty-vt.pc
%{_libdir}/cmake/ghostty-vt
