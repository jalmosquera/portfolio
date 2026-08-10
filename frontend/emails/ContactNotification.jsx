import {
  Body,
  Container,
  Head,
  Heading,
  Hr,
  Html,
  Preview,
  Section,
  Text,
} from 'react-email'

export default function ContactNotification({
  company = '{{ company_or_recruiter }}',
  email = '{{ email }}',
  phone = '{{ phone }}',
  description = '{{ description }}',
}) {
  return (
    <Html lang="es">
      <Head />
      <Preview>Nueva consulta desde tu portfolio</Preview>
      <Body style={body}>
        <Container style={container}>
          <Text style={eyebrow}>NUEVO CONTACTO</Text>
          <Heading style={heading}>Tenés una nueva consulta.</Heading>
          <Text style={intro}>Una empresa o reclutador completó el formulario de tu portfolio.</Text>
          <Hr style={divider} />
          <Section style={details}>
            <Text style={label}>Empresa o reclutador</Text>
            <Text style={value}>{company}</Text>
            <Text style={label}>Email</Text>
            <Text style={value}>{email}</Text>
            <Text style={label}>Teléfono</Text>
            <Text style={value}>{phone}</Text>
            <Text style={label}>Descripción</Text>
            <Text style={message}>{description}</Text>
          </Section>
          <Hr style={divider} />
          <Text style={footer}>Jalberth Mosquera · Portfolio backend</Text>
        </Container>
      </Body>
    </Html>
  )
}

const body = { backgroundColor: '#080808', fontFamily: 'Arial, sans-serif', margin: 0, padding: '32px 12px' }
const container = { backgroundColor: '#111111', border: '1px solid #2b2b2b', borderRadius: '12px', margin: '0 auto', maxWidth: '600px', padding: '32px' }
const eyebrow = { color: '#F17D34', fontSize: '12px', fontWeight: '700', letterSpacing: '2px', margin: '0 0 12px' }
const heading = { color: '#f5f5f5', fontSize: '28px', lineHeight: '1.25', margin: '0 0 12px' }
const intro = { color: '#a3a3a3', fontSize: '15px', lineHeight: '1.6', margin: 0 }
const divider = { borderColor: '#2b2b2b', margin: '24px 0' }
const details = { backgroundColor: '#0c0c0c', borderRadius: '8px', padding: '20px' }
const label = { color: '#F17D34', fontSize: '12px', fontWeight: '700', margin: '0 0 4px', textTransform: 'uppercase' }
const value = { color: '#f5f5f5', fontSize: '15px', lineHeight: '1.5', margin: '0 0 18px' }
const message = { ...value, marginBottom: 0, whiteSpace: 'pre-wrap' }
const footer = { color: '#737373', fontSize: '12px', margin: 0, textAlign: 'center' }
