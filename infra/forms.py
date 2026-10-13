from django import forms

from accounts.models import User
from core.security import clean_plain_text

from .models import InfraCalendarEvent, InfraRequest, InfraSector, TiInventoryItem, TiNetworkNode


class InfraRequestForm(forms.ModelForm):
    class Meta:
        model = InfraRequest
        fields = ('sector', 'category', 'title', 'location', 'asset_identifier', 'priority', 'description')
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Descreva o problema, o local, o equipamento e o impacto no trabalho.',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].label = 'Setor responsavel'
        self.fields['category'].label = 'Tipo de demanda'
        self.fields['title'].label = 'Titulo'
        self.fields['title'].widget.attrs.update({'placeholder': 'Ex.: Computador da secretaria nao liga'})
        self.fields['location'].label = 'Local'
        self.fields['location'].widget.attrs.update({'placeholder': 'Sala, campo, bloco, jardim ou casa'})
        self.fields['asset_identifier'].label = 'Maquina / equipamento'
        self.fields['asset_identifier'].required = False
        self.fields['asset_identifier'].widget.attrs.update({'placeholder': 'Opcional: patrimonio, nome da maquina, rede Wi-Fi'})
        self.fields['priority'].label = 'Prioridade'
        self.fields['description'].label = 'Descricao'

    def clean_title(self):
        return clean_plain_text(self.cleaned_data['title'])

    def clean_location(self):
        return clean_plain_text(self.cleaned_data['location'])

    def clean_asset_identifier(self):
        return clean_plain_text(self.cleaned_data.get('asset_identifier', ''))

    def clean_description(self):
        body = clean_plain_text(self.cleaned_data.get('description', ''))
        if not body:
            raise forms.ValidationError('Descreva a demanda para o setor de infra.')
        return body


class InfraRequestUpdateForm(forms.Form):
    body = forms.CharField(
        label='Mensagem',
        max_length=1800,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enviar mensagem para o solicitante ou operador'}),
    )

    def clean_body(self):
        body = clean_plain_text(self.cleaned_data.get('body', ''))
        if not body:
            raise forms.ValidationError('Escreva uma mensagem para registrar no dialogo.')
        return body


class InfraRequestManageForm(forms.ModelForm):
    class Meta:
        model = InfraRequest
        fields = ('status', 'priority', 'assigned_to', 'scheduled_for')
        widgets = {
            'scheduled_for': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('display_name', 'username')
        self.fields['assigned_to'].label = 'Operador responsavel'
        self.fields['assigned_to'].required = False
        self.fields['scheduled_for'].label = 'Agendamento'
        self.fields['scheduled_for'].required = False
        self.fields['scheduled_for'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['status'].label = 'Status'
        self.fields['priority'].label = 'Prioridade'


class InfraCalendarEventForm(forms.ModelForm):
    class Meta:
        model = InfraCalendarEvent
        fields = ('sector', 'title', 'start_at', 'end_at', 'location', 'responsible', 'status', 'notes')
        widgets = {
            'start_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, allowed_sectors=None, **kwargs):
        super().__init__(*args, **kwargs)
        if allowed_sectors is not None:
            self.fields['sector'].choices = [
                choice for choice in InfraSector.choices if choice[0] in set(allowed_sectors)
            ]
        self.fields['responsible'].queryset = User.objects.filter(is_active=True).order_by('display_name', 'username')
        self.fields['responsible'].required = False
        self.fields['sector'].label = 'Setor'
        self.fields['title'].label = 'Atividade'
        self.fields['start_at'].label = 'Inicio'
        self.fields['start_at'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end_at'].label = 'Fim'
        self.fields['end_at'].required = False
        self.fields['end_at'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['location'].label = 'Local'
        self.fields['responsible'].label = 'Responsavel'
        self.fields['status'].label = 'Status'
        self.fields['notes'].label = 'Observacoes'

    def clean_title(self):
        return clean_plain_text(self.cleaned_data['title'])

    def clean_location(self):
        return clean_plain_text(self.cleaned_data.get('location', ''))

    def clean_notes(self):
        return clean_plain_text(self.cleaned_data.get('notes', ''))


class TiSupportRequestForm(forms.ModelForm):
    class Meta:
        model = InfraRequest
        fields = ('category', 'title', 'location', 'asset_identifier', 'priority', 'description')
        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Explique o problema, a maquina ou rede afetada e quando percebeu a falha.',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [
            (InfraRequest.Category.COMPUTER, 'Computador / maquina'),
            (InfraRequest.Category.WIFI, 'Wi-Fi / rede'),
            (InfraRequest.Category.OTHER, 'Outro apoio de TI'),
        ]
        self.fields['category'].initial = InfraRequest.Category.COMPUTER
        self.fields['category'].label = 'Tipo de chamado'
        self.fields['title'].label = 'Resumo'
        self.fields['title'].widget.attrs.update({'placeholder': 'Ex.: Notebook da secretaria sem internet'})
        self.fields['location'].label = 'Local'
        self.fields['location'].widget.attrs.update({'placeholder': 'Sala, bloco, biblioteca, setor ou alojamento'})
        self.fields['asset_identifier'].label = 'Computador / rede'
        self.fields['asset_identifier'].required = False
        self.fields['asset_identifier'].widget.attrs.update({'placeholder': 'Opcional: patrimonio, nome do PC, SSID ou IP'})
        self.fields['priority'].label = 'Prioridade'
        self.fields['description'].label = 'Descricao'

    def clean_title(self):
        return clean_plain_text(self.cleaned_data['title'])

    def clean_location(self):
        return clean_plain_text(self.cleaned_data['location'])

    def clean_asset_identifier(self):
        return clean_plain_text(self.cleaned_data.get('asset_identifier', ''))

    def clean_description(self):
        body = clean_plain_text(self.cleaned_data.get('description', ''))
        if not body:
            raise forms.ValidationError('Descreva o chamado para a TI.')
        return body


class TiInventoryItemForm(forms.ModelForm):
    class Meta:
        model = TiInventoryItem
        fields = (
            'name',
            'kind',
            'asset_code',
            'location',
            'assigned_to',
            'ip_address',
            'mac_address',
            'operating_system',
            'status',
            'notes',
        )
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('display_name', 'username')
        self.fields['assigned_to'].required = False
        self.fields['name'].label = 'Nome do equipamento'
        self.fields['name'].widget.attrs.update({'placeholder': 'Ex.: PC-BIB-01'})
        self.fields['kind'].label = 'Tipo'
        self.fields['asset_code'].label = 'Patrimonio'
        self.fields['asset_code'].required = False
        self.fields['asset_code'].widget.attrs.update({'placeholder': 'Codigo de patrimonio, se houver'})
        self.fields['location'].label = 'Local'
        self.fields['location'].widget.attrs.update({'placeholder': 'Ex.: Biblioteca'})
        self.fields['assigned_to'].label = 'Usuario responsavel'
        self.fields['ip_address'].label = 'IP'
        self.fields['ip_address'].required = False
        self.fields['mac_address'].label = 'MAC'
        self.fields['mac_address'].required = False
        self.fields['operating_system'].label = 'Sistema operacional'
        self.fields['operating_system'].required = False
        self.fields['status'].label = 'Status'
        self.fields['notes'].label = 'Observacoes'
        self.fields['notes'].required = False

    def clean_name(self):
        return clean_plain_text(self.cleaned_data['name'])

    def clean_asset_code(self):
        return clean_plain_text(self.cleaned_data.get('asset_code', ''))

    def clean_location(self):
        return clean_plain_text(self.cleaned_data['location'])

    def clean_ip_address(self):
        return clean_plain_text(self.cleaned_data.get('ip_address', ''))

    def clean_mac_address(self):
        return clean_plain_text(self.cleaned_data.get('mac_address', ''))

    def clean_operating_system(self):
        return clean_plain_text(self.cleaned_data.get('operating_system', ''))

    def clean_notes(self):
        return clean_plain_text(self.cleaned_data.get('notes', ''))


class TiNetworkNodeForm(forms.ModelForm):
    class Meta:
        model = TiNetworkNode
        fields = ('name', 'kind', 'location', 'ip_address', 'ssid', 'vlan', 'upstream', 'status', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nome do ponto'
        self.fields['name'].widget.attrs.update({'placeholder': 'Ex.: AP Biblioteca'})
        self.fields['kind'].label = 'Tipo'
        self.fields['location'].label = 'Local'
        self.fields['location'].widget.attrs.update({'placeholder': 'Sala, bloco ou area coberta'})
        self.fields['ip_address'].label = 'IP'
        self.fields['ip_address'].required = False
        self.fields['ssid'].label = 'SSID'
        self.fields['ssid'].required = False
        self.fields['vlan'].label = 'VLAN / segmento'
        self.fields['vlan'].required = False
        self.fields['upstream'].label = 'Ligado a'
        self.fields['upstream'].required = False
        self.fields['upstream'].widget.attrs.update({'placeholder': 'Ex.: Switch central'})
        self.fields['status'].label = 'Status'
        self.fields['notes'].label = 'Observacoes'
        self.fields['notes'].required = False

    def clean_name(self):
        return clean_plain_text(self.cleaned_data['name'])

    def clean_location(self):
        return clean_plain_text(self.cleaned_data['location'])

    def clean_ip_address(self):
        return clean_plain_text(self.cleaned_data.get('ip_address', ''))

    def clean_ssid(self):
        return clean_plain_text(self.cleaned_data.get('ssid', ''))

    def clean_vlan(self):
        return clean_plain_text(self.cleaned_data.get('vlan', ''))

    def clean_upstream(self):
        return clean_plain_text(self.cleaned_data.get('upstream', ''))

    def clean_notes(self):
        return clean_plain_text(self.cleaned_data.get('notes', ''))
