import { LogIn } from 'lucide-react'
import { BrowserRouter , Route , Routes } from 'react-router-dom'
import Dashboard from './page/Dashboard'
import Login from './page/Login'

function App() {
  return (
    <>
    <BrowserRouter>
       <Routes>
       <Route path ="/" element ={<Login/>}></Route>
        <Route path ="/dashboard" element ={<Dashboard/>}></Route>
         
          
       </Routes>
    </BrowserRouter>
     
    </>
  )
}

export default App