# mental

Mental Survey 앱

API 서버 환경 
Django(https://www.djangoproject.com/)

기본 포트: 8000 
/mentalapi

프론트 환경
Vite(https://vitejs.dev/)

기본 포트: 4381
프록시: /mentalapi => localhost:8000


## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
pip install -r requirements.txt
npm install
```

### Compile and Hot-Reload for Development

```sh
python manage.py runserver 127.0.0.1:8000
vite
```

### Compile and Minify for Production

```sh
npm run build
```


--------------------------------------------------
## Project Setup

```sh
pip install -r requirements.txt
npm install
```

## Project Server Setting CheckList

mental/settings.py
    - ALLOWED_HOSTS : ['*']

package.json
    - scripts": {
            "dev": "vite --host 0.0.0.0 --port 8011",
        }

vite.config.js.json
    - server: {
            port: 8011,
            proxy: {'/mentalapi':'http://localhost:8010'}
        }

```sh
python manage.py runserver 0.0.0.0:8010
```
```sh
npm run dev
```