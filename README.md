![ml-model-diagram](https://github.com/JavierZam/ml-model-deployment/assets/69651946/e9d54969-1da7-4dfd-a703-3251c608ad75)

# ML Model Deployment

## Endpoint

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
