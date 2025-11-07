import { useState } from 'react'
import './App.css'
import CustomButton from './components/Button/CustomButton.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <CustomButton
        label="Submit"
        onClick={() => alert("Button clicked!")}
      />
    </div>
    </>
  )
}

export default App
