from django import forms
from .models import Chama

class ChamaForm(forms.ModelForm):
    class Meta:
        model = Chama
        fields = ['name', 'description', 'goal_amount']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your chama name (e.g., "Unity Savings Circle")',
                'maxlength': '100',
                'autocomplete': 'organization',
                'aria-label': 'Chama name',
                'data-field': 'name'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your chama goals, meeting frequency, member expectations, and investment focus...',
                'maxlength': '500',
                'aria-label': 'Chama description',
                'data-field': 'description'
            }),
            'goal_amount': forms.NumberInput(attrs={
                'placeholder': 'Enter target amount (e.g., 500000)',
                'min': '1000',
                'max': '10000000',
                'step': '1000',
                'aria-label': 'Goal amount in Kenyan Shillings',
                'data-field': 'goal_amount',
                'data-currency': 'KSH'
            }),
        }
        labels = {
            'name': 'Chama Name',
            'description': 'Description & Goals',
            'goal_amount': 'Target Savings Goal (KSH)',
        }
        help_texts = {
            'name': 'Choose a memorable and meaningful name that reflects your group\'s purpose and values.',
            'description': 'Provide comprehensive details about your chama to help potential members understand expectations, meeting schedules, and investment strategies.',
            'goal_amount': 'Set a realistic and motivating savings target that your group can achieve together. Consider your group size and contribution capacity.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom styling and attributes
        for field_name, field in self.fields.items():
            # Add common attributes
            field.widget.attrs.update({
                'data-field': field_name,
            })
            
            # Field-specific customizations
            if field_name == 'goal_amount':
                field.widget.attrs.update({
                    'data-currency': 'KSH',
                    'pattern': '[0-9,]+',
                    'title': 'Please enter a valid amount in Kenyan Shillings',
                    'oninput': 'formatCurrency(this)'
                })
            
            elif field_name == 'name':
                field.widget.attrs.update({
                    'oninput': 'updateCharacterCount("name", this.value, 100)',
                    'pattern': '[a-zA-Z0-9\\s\\-_]+',
                    'title': 'Only letters, numbers, spaces, hyphens, and underscores allowed'
                })
            
            elif field_name == 'description':
                field.widget.attrs.update({
                    'oninput': 'updateCharacterCount("description", this.value, 500)'
                })

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 3:
                raise forms.ValidationError("Chama name must be at least 3 characters long.")
            if len(name) > 100:
                raise forms.ValidationError("Chama name cannot exceed 100 characters.")
            
            # Check for inappropriate content (basic filter)
            inappropriate_words = ['test', 'fake', 'dummy']  # Add more as needed
            if any(word in name.lower() for word in inappropriate_words):
                raise forms.ValidationError("Please choose a more appropriate name for your chama.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            description = description.strip()
            if len(description) < 10:
                raise forms.ValidationError("Description must be at least 10 characters long.")
        return description

    def clean_goal_amount(self):
        goal_amount = self.cleaned_data.get('goal_amount')
        if goal_amount is not None:
            if goal_amount < 1000:
                raise forms.ValidationError("Goal amount must be at least 1,000 KSH.")
            if goal_amount > 10000000:  # 10 million KSH limit
                raise forms.ValidationError("Goal amount cannot exceed 10,000,000 KSH.")
        return goal_amount

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Clean and format data before saving
        if instance.name:
            instance.name = instance.name.strip().title()
        
        if instance.description:
            instance.description = instance.description.strip()
        
        if commit:
            instance.save()
        
        return instance