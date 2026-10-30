#include <iostream>
#include <cstdlib>
using std::cout;
using std::cin;

#ifdef _WIN32
#define CLS "cls"
#else
#define CLS "clear"
#endif

typedef struct simpul tsimpul;
struct simpul
{
    int info;
   tsimpul *next;
};
tsimpul *atas = NULL, *data, *hapus, *b1;
int jumlah=0;

void muncul()
{
    b1=atas;
   cout<<"\n        STACK ==>  ";
   if(atas==NULL)
   {
    cout<<"KOSONG";
   }
   while(b1!=NULL)
   {
    cout<<b1->info;
      b1=b1->next;
      cout<<"  ";
   }
   cout<<"\n        Jumlah Data : "<<jumlah;
}

void tambah_stack(int x)
{
   if(jumlah==10)
   {
        cout<<"Data Penuh!!!\n";
   }
   else
   {
    data=new simpul;
      data->info=x;
      data->next=atas;
      atas=data;
      jumlah++;
   }
}

void hapus_stack()
{
    if(atas==NULL)
   {
        cout<<"Maaf....Data Kosong!!!\n";
   }
   else
   {
      hapus=atas;
      atas=atas->next;
      jumlah--;
      cout<<"Penghapusan Berhasil\n";
   }
}

void hapus_semua()
{
    if(atas==NULL)
    {
        cout<<"Maaf....Data Kosong!!!\n";
   }
    else
    {
      while(atas!=NULL)
      {
        hapus=atas;
        atas=atas->next;
      }
      jumlah=0;
      cout<<"Semua Data Terhapus\n";
   }
}

int main()
{
   int pilih,n;
   char lagi;
   do
   {
      system(CLS);
      cout<<"================================================\n";
      cout<<"||              PROGRAM STACK                 ||\n";
      cout<<"================================================\n";
      muncul();
      cout<<"\n\n1. Tambah Data STACK";
      cout<<"\n2. Hapus Data Teratas";
      cout<<"\n3. Hapus Isi STACK";
      cout<<"\n4. Keluar Program\n==========================";
      cout<<"\nPilihan Anda : ";cin>>pilih;
      cout<<"==========================\n";
      switch(pilih)
    {
        case 1:
          cout<<"Masukkan Data    : ";cin>>n;
          tambah_stack(n);
          break;
        case 2:
          hapus_stack();
          break;
         case 3:
         hapus_semua();
         break;
         case 4:
         cout<<"\n SELESAI \n";
         cin.ignore();
         cin.get();
         return 0;
    }
    cout<<"Lagi (y/t)? ";cin>>lagi;
   }
   while(lagi=='y'||lagi=='Y');
   return 0;
}
