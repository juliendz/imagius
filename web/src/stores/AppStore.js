import { createContext } from 'react'
import { decorate, observable, computed } from 'mobx'

export class AppStore {
    watchedDirs = []

}

decorate(AppStore, {
    watchedDirs: observable,
})

export default createContext(new AppStore())