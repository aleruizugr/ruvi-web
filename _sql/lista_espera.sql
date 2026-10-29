-- Lista de espera de Dos Décimas, para opositores particulares (formulario de ruvilab.es/dos-decimas/)
-- Proyecto de Supabase: producción (lolqvimwnlikytbsnvsn).
--
-- NO SE HA EJECUTADO. Lo aplica el usuario a partir del 2 de noviembre, en
-- Supabase → SQL Editor. Después: poner LISTA_ABIERTA = True en _construir.py,
-- ejecutar «python3 _construir.py» y publicar.
--
-- Qué hace:
--   - crea la tabla lista_espera (email, fecha_examen, creado_en, consentimiento);
--   - activa RLS: desde la web (rol anon) solo se puede INSERTAR, nunca leer,
--     cambiar ni borrar. Los datos se consultan desde el panel de Supabase.
--   - el navegador solo puede rellenar email, fecha_examen y consentimiento;
--     creado_en lo pone la base de datos.
-- El guion está en una transacción: si algo falla, no queda nada a medias.
-- Se puede ejecutar dos veces sin romper nada.

begin;

create table if not exists public.lista_espera (
  id             bigint generated always as identity primary key,
  email          text        not null,
  fecha_examen   text        not null,
  creado_en      timestamptz not null default now(),
  consentimiento boolean     not null,
  constraint lista_espera_email_formato check (
    char_length(email) <= 254
    and email = lower(btrim(email))
    and email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'
  ),
  constraint lista_espera_fecha_valida check (fecha_examen in ('2027', 'mas_adelante', 'no_lo_se')),
  constraint lista_espera_con_consentimiento check (consentimiento = true)
);

-- Un email solo una vez. Si alguien se apunta de nuevo, la web recibe un 409
-- y le enseña el mismo mensaje de «te avisamos», sin decir si ya estaba.
create unique index if not exists lista_espera_email_unico on public.lista_espera (email);

comment on table public.lista_espera is
  'Lista de espera de Dos Décimas (ruvilab.es/dos-decimas/). Solo inserción desde la web. Borrar a petición o como máximo 12 meses después del alta.';

-- Permisos: quitar todo a los roles públicos y dar solo INSERT en las tres columnas del formulario.
revoke all on table public.lista_espera from anon, authenticated;
grant insert (email, fecha_examen, consentimiento) on table public.lista_espera to anon;

alter table public.lista_espera enable row level security;

drop policy if exists "lista_espera: insertar desde la web" on public.lista_espera;
create policy "lista_espera: insertar desde la web"
  on public.lista_espera
  for insert
  to anon
  with check (consentimiento = true);

-- No hay ninguna política de SELECT, UPDATE ni DELETE: con RLS activo, eso
-- significa que nadie las puede hacer desde la web. El panel de Supabase
-- (rol postgres / service_role) sí puede leer la tabla.

commit;

-- Comprobación tras aplicarlo (opcional, en el SQL Editor):
--   select relrowsecurity from pg_class where oid = 'public.lista_espera'::regclass;                       -- true
--   select policyname, cmd, roles from pg_policies where tablename = 'lista_espera';                      -- solo INSERT para anon
