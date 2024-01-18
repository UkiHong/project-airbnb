from django.db import models

# 생성한 다른 Model 들이 같은 value 를 가지도록 common model 을 만듦.
# django 는 models.py 를 확인할 때 마다 admin 패널에 추가하기 때문에
# 각 model은 common model 을 기본으로 가지지만 common model 자체는 admin panel 에 추가 x


class CommonModel(models.Model):
    # Common model definition

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Meta 는 django 에서 model 을 configure 할 때 사용
        # Meta 를 사용해서 django 가 이 common model을 데이터베이스에 저장하지 않음.
        abstract = True
