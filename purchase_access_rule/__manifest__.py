{
	'name': "Purchase Access Rule",
	'summary': "Access rule for purchase order and RFQ",
	'auther': "Muram Makkawi",
	'category':'Purchase',
	'depends': ['purchase'],
	'data': [
		'security/ir.model.access.csv',
		'security/purchase_security.xml'],
	'installable':True,
	'license': 'OEEL-1',

}