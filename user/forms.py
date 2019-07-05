from django import forms

from user.models import Profile


class ProfileForm(forms.ModelForm):
    #
    # def clean(self):
    #     return super().clean()

    def clean_max_distance(self):
        max_distance = self.cleaned_data.get('max_distance', 0)
        min_distance = self.cleaned_data.get('min_distance', 0)
        if max_distance < min_distance:
            raise forms.ValidationError('最大距离必须大于最小距离')

        return max_distance

    def clean_max_dating_age(self):
        max_dating_age = self.cleaned_data.get('max_dating_age', 0)
        min_dating_age = self.cleaned_data.get('min_dating_age', 0)
        if max_dating_age < min_dating_age:
            raise forms.ValidationError('最大年龄必须大于最小年龄')

        return max_dating_age

    class Meta:
        model = Profile
        fields = '__all__'
