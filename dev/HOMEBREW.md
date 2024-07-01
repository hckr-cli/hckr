# Homebrew formulae
* Local testing

## create a local tap for testing and link formulae
```shell
bash ./dev/brew.sh tap # this will create tap with latest source
```

## Testing
```shell
bash ./dev/brew.sh test
```

## style
```shell
bash ./dev/brew.sh style
```


* Bumping version [more](https://github.com/Homebrew/homebrew-core/blob/master/CONTRIBUTING.md)
```shell
brew bump-formula-pr --formula hckr
```
