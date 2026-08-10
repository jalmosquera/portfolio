import { Body, Container, Head, Heading, Hr, Html, Preview, Text } from 'react-email'

export default function ContactConfirmationEs({ company = '{{ company_or_recruiter }}' }) {
  return (
    <Html lang="es">
      <Head />
      <Preview>Recibí tu mensaje y me pondré en contacto pronto</Preview>
      <Body style={body}>
        <Container style={container}>
          <Text style={eyebrow}>MENSAJE RECIBIDO</Text>
          <Heading style={heading}>Gracias por contactarme.</Heading>
          <Text style={text}>Hola, {company}.</Text>
          <Text style={text}>Recibí correctamente tu mensaje. Revisaré la información y responderé lo antes posible.</Text>
          <Text style={text}>Si necesitás añadir algún detalle, podés responder directamente a este correo.</Text>
          <Hr style={divider} />
          <Text style={signature}>Jalberth Mosquera</Text>
          <Text style={role}>Backend Developer · Python & Django</Text>
        </Container>
      </Body>
    </Html>
  )
}

const body = { backgroundColor: '#080808', fontFamily: 'Arial, sans-serif', margin: 0, padding: '32px 12px' }
const container = { backgroundColor: '#111111', border: '1px solid #2b2b2b', borderRadius: '12px', margin: '0 auto', maxWidth: '600px', padding: '32px' }
const eyebrow = { color: '#F17D34', fontSize: '12px', fontWeight: '700', letterSpacing: '2px', margin: '0 0 12px' }
const heading = { color: '#f5f5f5', fontSize: '28px', lineHeight: '1.25', margin: '0 0 24px' }
const text = { color: '#c7c7c7', fontSize: '15px', lineHeight: '1.7', margin: '0 0 16px' }
const divider = { borderColor: '#2b2b2b', margin: '28px 0 20px' }
const signature = { color: '#f5f5f5', fontSize: '15px', fontWeight: '700', margin: '0 0 4px' }
const role = { color: '#F17D34', fontSize: '13px', margin: 0 }
