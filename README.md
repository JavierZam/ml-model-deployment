# ML Model Deployment

## Endpoint

- base url: https://ml-model-deployment-ymrdyfncwq-et.a.run.app/

- Path : `/predict/{userId}`
- Method : `POST`
- Request Body (form-data) :
  - file as `image`, jpg format
- Response :

```json
{
  "nama": "air",
  "kalori": 0,
  "satuan": "ml",
  "image_url": "https://storage.googleapis.com/foods-image/5TcC8rY4L7VsSR2lWAZiVnDDSgy2/AwMHLB3kXFV8pL6bWMmu"
}
```
