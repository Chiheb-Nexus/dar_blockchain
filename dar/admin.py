from django.contrib import admin
from . import models

@admin.register(models.AlimentationProduit)
class AlimentationProduitAdmin(admin.ModelAdmin):
	list_display = ('dar', 'produit', 'quantity', 'prix', 'date')

class AlimentationProduitInline(admin.TabularInline):
	model = models.AlimentationProduit
	extra = 0

@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
	list_display = ('code_promotion',)
	
class PromotionInline(admin.TabularInline):
	model = models.Promotion
	extra = 0

@admin.register(models.CodePromotion)
class CodePromotionAdmin(admin.ModelAdmin):
	list_display = ('code_promotion', 'percent_reduced', 'date_debut', 'date_fin')
	inlines = (PromotionInline,)

@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
	list_display = ('salle', 'date_debut', 'date_fin', 'client', 'panier')
	inlines = (PromotionInline,)

class ReservationInline(admin.TabularInline):
	model = models.Reservation
	extra = 0

@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('produit', 'quantity', 'panier')

class TransactionInline(admin.TabularInline):
	model = models.Transaction
	extra = 0

@admin.register(models.ProduitSalle)
class ProduitSalleAdmin(admin.ModelAdmin):
	list_display = ('salle', 'alimentation_produit', 'quantity', 'price')

class ProduitSalleInline(admin.TabularInline):
	model = models.ProduitSalle
	extra = 0

@admin.register(models.Produit)
class ProduitAdmin(admin.ModelAdmin):
	list_display = ('nom','_uuid')
	inlines = (
		AlimentationProduitInline, 
		PromotionInline
	)

class ProduitInline(admin.TabularInline):
	model = models.Produit 
	extra = 0

@admin.register(models.Panier)
class PanierAdmin(admin.ModelAdmin):
	list_display = ('_uuid','dar', 'user', 'date', 'tx_hash')
	inlines = (TransactionInline, ReservationInline)

class PanierInline(admin.TabularInline):
	model = models.Panier
	extra = 0

@admin.register(models.Salle)
class SalleAdmin(admin.ModelAdmin):
	list_display = ('dar', 'nom_salle', 'user', 'fonction_salle', 'price', 'salle_prof','_uuid')
	inlines = (ProduitSalleInline, ReservationInline)

class SalleInline(admin.TabularInline):
	model = models.Salle 
	extra = 0

@admin.register(models.Pack)
class PackAdmin(admin.ModelAdmin):
	list_display = ('titre', 'informations', 'price')

class PackAdminInline(admin.TabularInline):
	model = models.Pack
	extra = 0

@admin.register(models.Dyar)
class DyarAdmin(admin.ModelAdmin):
	list_display = ('nom', 'address')
	inlines = (
		PackAdminInline, 
		SalleInline, 
		PromotionInline,
		AlimentationProduitInline,
		PanierInline,
	)

@admin.register(models.Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
	list_display = ('pack', 'user_abonne', 'date_debut', 'date_fin', 'is_group')

class AbonnementInline(admin.TabularInline):
	model = models.Abonnement
	extra = 0

@admin.register(models.DarUser)
class DarUserAdmin(admin.ModelAdmin):
	list_display = ('dar',  'user', 'solde', 'is_admin', 'is_client', 'is_abonn','_uuid')
	inlines = (SalleInline, AbonnementInline, PanierInline, ReservationInline)

@admin.register(models.Fonction)
class FonctionAdmin(admin.ModelAdmin):
	list_display = ('fonction_name', 'description')
	inlines = (SalleInline,)

@admin.register(models.Formation)
class FormationAdmin(admin.ModelAdmin):
	list_display = ('_uuid','titre','description')

@admin.register(models.FormationDar)
class FormationDarAdmin(admin.ModelAdmin):
	list_display = ('formateur','salle','formation')
@admin.register(models.TransactionFormation)
class TransactionFormationAdmin(admin.ModelAdmin):
	list_display = ('_uuid','user','current_date','formation_dar','panier')