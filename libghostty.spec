%define libname %mklibname ghostty-vt
%define devname %mklibname ghostty-vt -d

Name:		%{libname}
Version:	1.4.0
Release:	1
Summary:	Ghostty terminal emulation library
Url:		https://ghostty.org/
License:	MIT and Apache-2.0 and CC0-1.0
Group:		System/Libraries
Source0:	https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
# Extracted zig packages, named by the bare hash. zig --system rejects tarballs.
Source1:	ghostty-%{version}-zig-packages.tar.xz
# zig 0.17 ships a broken amxtf32intrin.h. Skip it while compiling wuffs.
Patch0:		ghostty-%{version}-zig-amx-tf32.patch
BuildRequires:	zig >= 0.17.0

%description
Shared terminal emulation library from Ghostty. KDE terminal
applications link this library. The Ghostty GTK application is not
included.

%package -n %{devname}
Summary:	Development files for %{libname}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Header files for %{libname}.

%prep
%autosetup -p1 -n ghostty-%{version} -a 1
cp -a LICENSE LICENSE.ghostty
cp -a p/N-V-__8AAP5JWgCGP_AD0teWpa4krRvE9VPZzvviGdbmN4jI/LICENSE LICENSE.wuffs
cp -a p/N-V-__8AADYiAAB_80AWnH1AxXC0tql9thT-R-DYO1gBqTLc/LICENSE LICENSE.pixels
cp -a p/uucode-0.2.0-ZZjBPoGFVgCiflJNFc6Io8xzC67B6PA5bUkk4LT0kCxg/LICENSE.md LICENSE.uucode

%install
# SIMD stays off: zig 0.17 cannot compile the bundled simdutf and highway.
# Ghostty bakes DESTDIR into prefix and hardcodes libdir as ${prefix}/lib.
DESTDIR="%{buildroot}" \
ZIG_GLOBAL_CACHE_DIR="%{_builddir}/zig-global-cache" \
zig build \
	--cache-dir "%{_builddir}/zig-local-cache" \
	--system "$PWD/p" \
	--build-id=sha1 \
	-Demit-lib-vt \
	-Dsimd=false \
	-Demit-themes=false \
	-Demit-terminfo=false \
	-Dapp-runtime=none \
	-Di18n=false \
	-Doptimize=ReleaseFast \
	-Dcpu=baseline \
	-Dversion-string=%{version} \
	--prefix %{_prefix} \
	--prefix-lib-dir %{_lib}
sed -i \
	-e 's|^prefix=.*|prefix=%{_prefix}|' \
	-e 's|^libdir=.*|libdir=%{_libdir}|' \
	%{buildroot}%{_datadir}/pkgconfig/libghostty-vt.pc
rm -f %{buildroot}%{_libdir}/libghostty-vt.a \
	%{buildroot}%{_datadir}/pkgconfig/libghostty-vt-static.pc

%files
%license LICENSE.ghostty LICENSE.wuffs LICENSE.pixels LICENSE.uucode
%{_libdir}/libghostty-vt.so.0*

%files -n %{devname}
%{_includedir}/ghostty
%{_libdir}/libghostty-vt.so
%{_datadir}/pkgconfig/libghostty-vt.pc
