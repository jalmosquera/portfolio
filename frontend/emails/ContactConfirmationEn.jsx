import { Body, Container, Head, Heading, Hr, Html, Preview, Text } from 'react-email'

export default function ContactConfirmationEn({ company = '{{ company_or_recruiter }}' }) {
  return (
    <Html lang="en">
      <Head />
      <Preview>I received your message and will get back to you soon</Preview>
      <Body style={body}>
        <Container style={container}>
          <Text style={eyebrow}>MESSAGE RECEIVED</Text>
          <Heading style={heading}>Thank you for reaching out.</Heading>
          <Text style={text}>Hello, {company}.</Text>
          <Text style={text}>Your message was received successfully. I will review the information and reply as soon as possible.</Text>
          <Text style={text}>If you need to add any details, you can reply directly to this email.</Text>
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
