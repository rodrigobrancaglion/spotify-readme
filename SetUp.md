# Set Up

## Spotify API App

- Create a [Spotify Application](https://developer.spotify.com/dashboard/applications)
- Take note of:
    - `Client ID`
    - `Client Secret`
- Click on **Edit Settings**
- In **Redirect URIs**:
    - Add `http://localhost/callback/`

## Refresh Token

### Powershell

<details>

<summary>Script to complete this section</summary>

```powershell
# Request Client ID and Client Secret from the user
$ClientId = Read-Host "Enter the Client ID"
$ClientSecret = Read-Host "Enter the Client Secret"

# Generate authorization URL with the required scopes
$RedirectUri = "http://localhost/callback/"
$Scope = "user-read-currently-playing user-read-recently-played"
$AuthorizationUrl = "https://accounts.spotify.com/authorize?client_id=$ClientId&response_type=code&scope=$([uri]::EscapeDataString($Scope))&redirect_uri=$([uri]::EscapeDataString($RedirectUri))"

# Open the URL in the browser to obtain the authorization code
Write-Host "Opening browser for authorization..."
Start-Process $AuthorizationUrl

# Request the authorization code obtained after login
$Code = Read-Host "Please enter the authorization code (part after '?code=' in the URL)"

# Generate Base64 string for authentication
$ClientBytes = [System.Text.Encoding]::UTF8.GetBytes("${ClientId}:${ClientSecret}")
$EncodedClientInfo = [Convert]::ToBase64String($ClientBytes)

# Make the request to obtain tokens (access_token and refresh_token)
$Response = Invoke-WebRequest -Uri "https://accounts.spotify.com/api/token" `
                               -Method POST `
                               -Headers @{
                                   "Authorization" = "Basic $EncodedClientInfo"
                                   "Content-Type" = "application/x-www-form-urlencoded"
                               } `
                               -Body "grant_type=authorization_code&redirect_uri=$([uri]::EscapeDataString($RedirectUri))&code=$Code"

# Process the response
$ResponseData = $Response.Content | ConvertFrom-Json

# Display the tokens to the user
Write-Host "`nAccess Token:" $ResponseData.access_token
Write-Host "`nRefresh Token:" $ResponseData.refresh_token

# Save tokens in variables for reuse
$AccessToken = $ResponseData.access_token
$RefreshToken = $ResponseData.refresh_token

# Confirm that the tokens were obtained successfully
Write-Host "`nTokens obtained successfully!"

```

</details>

### Manual

- Navigate to the following URL:

```
https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&scope=user-read-currently-playing,user-read-recently-played&redirect_uri=http://localhost/callback/
```

- After logging in, save the {CODE} portion of: `http://localhost/callback/?code={CODE}`

- Create a string combining `{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}` (e.g. `5n7o4v5a3t7o5r2e3m1:5a8n7d3r4e2w5n8o2v3a7c5`) and **encode** into [Base64](https://base64.io/).

- Then run a [curl command](https://httpie.org/run) in the form of:

```sh
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: Basic {BASE64}" -d "grant_type=authorization_code&redirect_uri=http://localhost/callback/&code={CODE}" https://accounts.spotify.com/api/token
```

- Save the Refresh token

## Deployment

### Deploy to Vercel

- Register on [Vercel](https://vercel.com/)

- Fork this repo, then create a vercel project linked to it

- Add Environment Variables:

    - `https://vercel.com/<YourName>/<ProjectName>/settings/environment-variables`
        - `SPOTIFY_REFRESH_TOKEN`
        - `SPOTIFY_CLIENT_ID`
        - `SPOTIFY_SECRET_ID`

- Deploy!


## Add to Your Readme

```md
### Spotify Playing 🎧

[<img src="https://<YOUR VERCEL SERVER URL>/api/spotify-playing" alt="Spotify Now Playing" width="350" />](https://open.spotify.com/user/<YOUR SPOTIFY USER ID>)
```

<!--
### Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https%3A%2F%2Fgithub.com%2Fnovatorem%2Fnovatorem)

- Create a Heroku application via the Heroku CLI or via the Heroku Dashboard. Connect the app with your GitHub repository and enable automatic builds <br>
  `PS. automatic build means that everytime you push changes to remote, heroku will rebuild and redeploy the app.`
    - To start the Flask server execute `heroku ps:scale web=1` once the build is completed.
- Or click the `Deploy to Heroku` button above to automatically start the deployment process.

### Run locally with Docker

- You need to have [Docker](https://docs.docker.com/get-docker/) installed.

- Add Environment Variables:
    - `SPOTIFY_REFRESH_TOKEN`
    - `SPOTIFY_CLIENT_ID`
    - `SPOTIFY_SECRET_ID`
- To run the service, open a terminal in the root folder of the repo: <br>
  Execute:
  ```
  docker compose up
  ```
- When finished, navigate to [http://localhost:5000/](http://localhost:5000/)
- To stop the service, open a terminal in the root folder of the repo: <br>
  Execute:
  ```
  docker compose down
  ```

## ReadMe

You can now use the following in your readme:

`[![Spotify](https://USER_NAME.vercel.app/api/spotify)](https://open.spotify.com/user/USER_NAME)`

## Customization

### Hide the EQ bar

Remove the `#` in front of `contentBar` in [line 81](https://github.com/novatorem/novatorem/blob/98ba4a8489ad86f5f73e95088e620e8859d28e71/api/spotify.py#L81) of current master, then the EQ bar will be hidden when you're in not currently playing anything.

### Status String

Have a string saying either "Vibing to:" or "Last seen playing:".

- Change [`height` to `height + 40`](https://github.com/novatorem/novatorem/blob/5194a689253ee4c89a9d365260d6050923d93dd5/api/templates/spotify.html.j2#L1-L2) (or whatever `margin-top` is set to)
- Uncomment [**.main**'s `margin-top`](https://github.com/novatorem/novatorem/blob/5194a689253ee4c89a9d365260d6050923d93dd5/api/templates/spotify.html.j2#L10)
- Uncomment [currentStatus](https://github.com/novatorem/novatorem/blob/5194a689253ee4c89a9d365260d6050923d93dd5/api/templates/spotify.html.j2#L93)
-->
### Theme Templates

If you want to change the widget theme, you can do so by the changing the `current-theme` property in the `templates.json` file.

Themes:

- `light`
- `dark`

If you wish to customize farther, you can add your own customized `spotify.html.j2` file to the templates folder, and add the theme and file name to the `templates` dictionary in the `templates.json` file.

### Color

You can customize the appearance of your `Card` however you wish with URL params.

#### Common Options:

- `background_color` - Card's background color _(hex color)_ without `#`
- `border_color` - Card border color _(hex color)_ without `#`

Use `/?background_color=8b0000&border_color=ffffff` parameter like so:  
&nbsp; <br> [![Spotify](https://spotify-readme-rodrigobrancaglions.vercel.app/api/spotify-playing?background_color=0d1117&border_color=ffffff)]()

### Spotify Logo

You can add the spotify logo by removing the commented out code, seen below:

```html
<a href="{{songURI}}" class="spotify-logo">
  <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <title>Spotify</title>
    <path
      d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"
    />
  </svg>
</a>
```

## Requests

Customization requests can be submitted as an issue, like https://github.com/novatorem/novatorem/issues/2

If you want to share your own customization options, open a PR if it's done or open an issue if you want it implemented by someone else.

## Debugging

If you have issues setting up, try following this [guide](https://youtu.be/n6d4KHSKqGk?t=615).

Followed the guide and still having problems?
Try checking out the functions tab in vercel, linked as:
`https://vercel.com/{name}/spotify/{build}/functions`

<details><summary>Which looks like</summary>

![image](https://user-images.githubusercontent.com/16753077/91338931-b0326680-e7a3-11ea-8178-5499e0e73250.png)

</details><br>

You will see a log there, and most issues can be resolved by ensuring you have the correct variables from setup.