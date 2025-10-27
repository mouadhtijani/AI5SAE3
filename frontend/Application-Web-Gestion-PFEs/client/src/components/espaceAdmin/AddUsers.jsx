import React, { useState } from 'react';
import SideBareAdmin from './SideBareAdmin';
import Header from '../Header';
import { Link } from "react-router-dom";

const AddUsers = () => {
  const [full_name, setFullName] = useState('');
  const [specialite, setSpecialite] = useState(''); // ← sera utilisé comme "role"
  const [email, setEmail] = useState('');

  // Champs pour l'IA
  const [skill1, setSkill1] = useState('');
  const [skill2, setSkill2] = useState('');
  const [skill3, setSkill3] = useState('');
  const [workload, setWorkload] = useState(0.0);

  async function nouveauUser(e) {
    e.preventDefault();

    const userData = {
      full_name,
      email,
      role: specialite, // ✅ specialite devient le "role" dans le backend
      skill1,
      skill2: skill2 || undefined,
      skill3: skill3 || undefined,
      workload: parseFloat(workload) || 0.0
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/api/tasks/users/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });

      if (response.ok) {
        alert('Utilisateur ajouté avec succès !');
        // Réinitialiser le formulaire
        setFullName('');
        setSpecialite('');
        setEmail('');
        setSkill1('');
        setSkill2('');
        setSkill3('');
        setWorkload(0.0);
      } else {
        const error = await response.json();
        alert('Erreur: ' + (error.detail || 'Échec de l’ajout'));
      }
    } catch (err) {
      console.error(err);
      alert('Erreur réseau. Vérifiez que le backend est lancé.');
    }
  }

  return (
    <>
      <div className='flex'>
        <SideBareAdmin />
        <div className='h-full w-full'>
          <Header />
          <div className='h-[90%] flex flex-col justify-around items-center'>
            <h2 className='text-xl font-bold py-4'>Ajouter un utilisateur :</h2>
            <form className='flex flex-col justify-center gap-y-4 w-[75%]' onSubmit={nouveauUser}>
              <input
                placeholder='Nom complet'
                className='border-black border-2 rounded-lg pl-2 h-9'
                value={full_name}
                onChange={e => setFullName(e.target.value)}
                required
              />
              <input
                placeholder='Spécialité (sera utilisée comme rôle)'
                className='border-black border-2 rounded-lg pl-2 h-9'
                value={specialite}
                onChange={e => setSpecialite(e.target.value)}
                required
              />
              <input
                placeholder='Email'
                type='email'
                className='border-black border-2 rounded-lg pl-2 h-9'
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
              />

              {/* --- Compétences pour l'IA --- */}
              <input
                placeholder='Compétence 1 (requise)'
                className='border-black border-2 rounded-lg pl-2 h-9'
                value={skill1}
                onChange={e => setSkill1(e.target.value)}
                required
              />
              <input
                placeholder='Compétence 2 (optionnelle)'
                className='border-black border-2 rounded-lg pl-2 h-9'
                value={skill2}
                onChange={e => setSkill2(e.target.value)}
              />
              <input
                placeholder='Compétence 3 (optionnelle)'
                className='border-black border-2 rounded-lg pl-2 h-9'
                value={skill3}
                onChange={e => setSkill3(e.target.value)}
              />
              <input
                placeholder='Charge de travail (0.0 à 1.0)'
                type='number'
                min='0'
                max='1'
                step='0.1'
                className='border-black border-2 rounded-lg pl-2 h-9'
                value={workload}
                onChange={e => setWorkload(e.target.value)}
                required
              />

              <div className='flex gap-x-3 justify-end h-11'>
                <Link to='/Admin/ListUsers' className='bg-red-500 w-[20%] rounded-lg flex justify-center'>
                  <button type='button'>Annuler</button>
                </Link>
                <button className='bg-green-500 w-[20%] rounded-lg' type='submit'>
                  Ajouter
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
};

export default AddUsers;