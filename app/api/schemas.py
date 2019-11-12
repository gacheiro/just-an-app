from marshmallow import Schema, fields, validate


class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    firebase_id = fields.Str(dump_only=True)
    nome = fields.Str(validate=validate.Length(max=80))
    email = fields.Str(validate=validate.Length(max=120))
    criado_em = fields.Date(dump_only=True)


class ViagemSchema(Schema):
    id = fields.Int(dump_only=True)
    usuario = fields.Nested(UsuarioSchema, dump_only=True)
    de = fields.Str(validate=validate.Length(max=100))
    para = fields.Str(validate=validate.Length(max=100))
    data = fields.Date()
    criado_em = fields.Date(dump_only=True)
