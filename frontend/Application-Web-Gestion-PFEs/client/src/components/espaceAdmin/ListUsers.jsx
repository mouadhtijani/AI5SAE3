import React, { useEffect, useState } from 'react';
import SideBareAdmin from './SideBareAdmin';
import CartUser from './CartUser';
import { TbSearch } from 'react-icons/tb';
import Header from '../Header';
import { Link } from "react-router-dom";

const ListUsers = () => {
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Fetch users from FastAPI backend
    fetch('http://127.0.0.1:8000/api/tasks/users/', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch users');
        return res.json();
      })
      .then(data => {
        setData(data);
      })
      .catch(err => {
        console.error(err);
        alert('Erreur lors du chargement des utilisateurs');
      });
  }, []);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredData = data.filter((item) =>
    item.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.role?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (item.skills && item.skills.some(skill =>
      skill.toLowerCase().includes(searchTerm.toLowerCase())
    ))
  );

  return (
    <div className='flex'>
      <SideBareAdmin />

      <div className='h-full w-full'>
        <Header />
        
        <form className='flex justify-end mr-7'>
          <div className='relative flex items-center pt-4'>
            <input
              type="text"
              placeholder="Rechercher..."
              value={searchTerm}
              onChange={handleSearch}
              className='pl-6 border-2 border-black rounded-lg h-8 w-64'
            />
            <TbSearch className='absolute right-3 text-sky-400 text-xl' />
          </div>
        </form>

        <div className='flex gap-x-3 h-11 pl-6'>
          <Link to='/Admin/AddUsers'>
            <button className='bg-green-500 p-1 w-[80px] rounded-lg' type='submit'>
              Ajouter
            </button>
          </Link>
        </div>

        <div className='h-[80%]'>
          <h2 className='font-medium text-xl pl-6'>Utilisateurs :</h2>
          <div className='w-[70%] mx-auto border-2 border-black rounded-md h-[30rem] overflow-scroll scrollbar scrollbar-thumb-sky-500 scrollbar-thin'>
            {filteredData.length > 0 ? (
              filteredData.map((item, index) => (
                <CartUser
                key={item.name}
                  name={item.name}
                  email={item.email}   // ✅
                  role={item.role}
                  skills={item.skills}
                  workload={item.workload}
                />    
              ))
            ) : (
              <div className="p-4 text-center text-gray-500">Aucun utilisateur trouvé</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ListUsers;