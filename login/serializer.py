from rest_framework import serializers
from login.models import CustomUser


class UserSignUP(serializers.ModelSerializer):
    # we are writing this becoz we need confirm password field in our registration request
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model= CustomUser
        fields = ['email','password','password2','first_name','last_name','address','phone_number']
        extra_kwargs={
            'password':{'write_only':True}
        }

        # Validating Password and Confirm Password while Registration

    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("confirm password doesn't match")
        return attrs
        
    def create(self,validate_data):
        return CustomUser.objects.create_user(**validate_data)


class UserLogin(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = CustomUser
        fields = [ 'email','password']


# to view it's name using token
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields=['id','email','name']

# for changing password ## late feature
class UserChangePasswordSerializer(serializers.Serializer): 
    password = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)

    class Meta:
        fields=['password','password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError("confirm password doesn't match")
        user.set_password(password)
        user.save()
        return attrs







