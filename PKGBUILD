# Maintainer: Timothy Brown <sysop@timb.us>

pkgname=raspberrypi-bluetooth
pkgver=1.0.0
pkgrel=1
epoch=
pkgdesc="Provides Bluetooth support for Raspberry Pi 3B/3B+/ZeroW without using legacy Bluez tools."
arch=('armv6h' 'armv7h' 'aarch64')
url="http://github.com/timothybrown/raspberrypi-bluetooth"
license=('MIT')
groups=()
depends=('bluez' 'bluez-utils' 'python' 'python-systemd')
makedepends=('python-pip' 'python-setuptools' 'python-wheel')
source=("$pkgname-$pkgver.py"
        "$pkgname-$pkgver.service"
        "rpinfo-0.2.1.tar.gz")
noextract=("rpinfo-0.2.1.tar.gz")
md5sums=('15f8a2d3a1eb39a2568e03489fe2385b'
         '90674910d8a23d4ba7ca2bd068fb55a4'
         '202bec3ad07cb05a120359fa92ce802c')
package() {
	pip install --root $pkgdir $srcdir/rpinfo-0.2.1.tar.gz
	install -d "$pkgdir/usr/bin" "$pkgdir/usr/lib/systemd/system"
	install -m 755 "$srcdir/$pkgname-$pkgver.py" "$pkgdir/usr/bin/raspberrypi-bluetooth"
	install -m 644 "$srcdir/$pkgname-$pkgver.service" "$pkgdir/usr/lib/systemd/system/raspberrypi-bluetooth.service"
}