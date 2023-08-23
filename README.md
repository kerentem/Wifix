
# Wifix

Save big on costs with our complete Wi-Fi network solution for businesses!




## Authors

- [@michaelkosoy](https://www.github.com/michaelkosoy)
- [@kerentem](https://www.github.com/kerentem)
- [@BarSela98](https://www.github.com/BarSela98)
- [@yotamhr](https://www.github.com/yotamhr)

![Logo](https://static.wixstatic.com/media/827475_d5d11b690c7e4b3a871182548f031320~mv2.png/v1/fill/w_274,h_161,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/H7900532_logos_72_dpi_HE.png)


## Features

- Live analytics
- Dynamic pricing model
- Friendly easy-to-use UI
- Active load balancing


## Acknowledgements

 - [MTA - The accademic college of Tel-Aviv-Jaffo](https://www.mta.ac.il/he-il/)
 - [Mentor - Hadar Binsky](hbinsky.mta@gmail.com‏)

## Demo

https://www.youtube.com/watch?v=ZdZqr9GWKaQ&embeds_referring_euri=https%3A%2F%2Fdocs.google.com%2F&embeds_referring_origin=https%3A%2F%2Fdocs.google.com&source_ve_path=MjM4NTE&feature=emb_title

## API Reference
https://app.swaggerhub.com/apis/BARSELA/wifix/1.0.0#/User/get_wifi_session_is_expired

Mostly used API's are:
#### 1.Register a new user

```http
  POST /admin/register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `None` | `string` | Adds a new user the the DB |

#### 2.Expired WIFI session

```http
  GET /wifi_session/is_expired
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `json` | Check if WIFI session is expired for a user |



