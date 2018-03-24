
pushd src\imagius && (

    pyinstaller imagius.spec --noconfirm --workpath=../../build --distpath=../../dist
    popd
    xcopy.exe resources\images\imagius.ico dist\imagius\
)
