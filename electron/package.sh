#!/usr/bin/env bash


appName="707danmu"
packagePath="707danmu*"

rm -rf $packagePath

if [ $# -lt 1 ]; then
    sh package.sh --help
    return
fi

case $1 in
    'help' | '--help' )
        echo 'Usage: sh package.sh -p <platform>'
        echo '  -p:  w32, w64, l32, l64, osx'
        echo 'Example: package.sh -p osx'
        return
    ;;

    '-p' )
        cd app && npm i && cd ..
        case $2 in
            w32 )
                electron-packager app $appName --platform=win32 --arch=ia32
            ;;

            w64 )
                electron-packager app $appName --platform=win32 --arch=x64
            ;;

            l32 )
                electron-packager app $appName --platform=linux --arch=ia32
            ;;

            l64 )
                electron-packager app $appName --platform=linux --arch=x64
            ;;

            osx )
                electron-packager app $appName --platform=darwin --arch=x64
            ;;

            * )
                sh package.sh --help
                return
            ;;
        esac
    ;;
esac

cd $packagePath
