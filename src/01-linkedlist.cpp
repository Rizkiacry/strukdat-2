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
tsimpul *awal = NULL, *akhir = NULL, *data, *hapus, *b1, *b2;

void muncul()
{
    b1=awal;
   cout<<"\n        DATA ==>  ";
   while(b1!=NULL)
   {
    cout<<b1->info;
      b1=b1->next;
      cout<<"  ";
   }
}

void tambah_awal(int x)
{
   data=new simpul;
   data->info=x;
   data->next=NULL;
   if(awal==NULL)
   {
    awal=akhir=data;
   }
   else
   {
    data->next=awal;
      awal=data;
   }
}

void tambah_akhir(int x)
{
   data=new simpul;
   data->info=x;
   data->next=NULL;
   if(awal==NULL)
   {
        awal=akhir=data;
   }
   else
   {
    akhir->next=data;
      akhir=data;
   }
}

void tambah_tengah(int in,int setelah)
{
    b1=awal;
   int ada=0;
   while (b1 != NULL)
   {
        if (b1->info == setelah)
        {
            ada++;
        }
        b1 = b1->next;
   }
   if(ada==0)
    cout<<"\n-->Data Yang Di Masukkan Tidak valid<--\n\n";
   else
   {
    b1=awal;
       b2=b1->next;
    while(b1->info!=setelah)
    {
        b1=b1->next;
        b2=b1->next;
    }
        data=new simpul;
    data->info=in;
      b1->next=data;
      if(b1==akhir)
      {
         akhir=data;
      }
      data->next=b2;
   }
}

void hapus_awal()
{
    if(awal==NULL)
   {
        cout<<"Maaf....List Kosong!!!\n";
   }
   else
   {
      hapus=awal;
      awal=awal->next;
      if(awal==NULL)
      {
        akhir=NULL;
      }
      delete hapus;
      hapus=NULL;
      cout<<"Hapus Awal Berhasil\n";
   }
}

void hapus_akhir()
{
    if(awal==NULL)
   {
        cout<<"Maaf....List Kosong!!!\n";
   }
    else if(awal==akhir)
    {
    hapus=awal;
    awal=NULL;
    akhir=NULL;
    delete hapus;
    hapus=NULL;
    cout<<"Hapus Akhir Berhasil\n";
   }
   else
   {
        b1=awal;
      while(b1->next!=akhir)
      {
        b1=b1->next;
      }
      hapus=akhir;
      b1->next=NULL;
      akhir=b1;
      delete hapus;
      hapus=NULL;
      cout<<"Hapus Akhir Berhasil\n";
   }
}

void hapus_tengah(int x)
{
    tsimpul *b;
   if(awal==NULL)
        cout<<"Maaf....List Kosong!!!\n";
   else if(awal->info==x)
        hapus_awal();
   else
   {
      b=awal;
      while(b->next!=NULL && b->next->info!=x)
      {
        b=b->next;
      }
      if(b->next==NULL)
            cout<<"\n-->Data Yang Di Masukkan Tidak Valid<--\n\n";
      else
      {
        hapus=b->next;
        b->next=hapus->next;
        if(hapus==akhir)
        {
            akhir=b;
        }
        delete hapus;
        hapus=NULL;
        cout<<"Hapus Tengah Berhasil\n";
      }
   }
}

int main()
{
   int pilih,n,nn;
   char lagi;
   do
   {
      system(CLS);
      cout<<"================================================\n";
      cout<<"||         PROGRAM SINGLE LINKED LIST         ||\n";
      cout<<"================================================\n";
      muncul();
      cout<<"\n\n1. Tambah Awal";
      cout<<"\n2. Tambah Akhir";
      cout<<"\n3. Tambah Tengah";
      cout<<"\n4. Hapus Awal";
      cout<<"\n5. Hapus Akhir";
      cout<<"\n6. Hapus Tengah\n==========================";
      cout<<"\nPilihan Anda : ";cin>>pilih;
      cout<<"==========================\n";
      switch(pilih)
    {
        case 1:
          cout<<"Masukkan Data    : ";cin>>n;
          tambah_awal(n);
          break;
        case 2:
          cout<<"Masukkan Data    : ";cin>>n;
          tambah_akhir(n);
          break;
        case 3:
          cout<<"Masukkan Data    : ";cin>>n;
          cout<<"Dimasukkan Setelah : ";cin>>nn;
          tambah_tengah(n,nn);
          break;
        case 4:
         hapus_awal();
         break;
         case 5:
         hapus_akhir();
         break;
         case 6:
         cout<<"data yg ingin di hapus : ";cin>>nn;
         hapus_tengah(nn);
         break;
    }
    cout<<"Lagi (y/t)? ";cin>>lagi;
   }
   while(lagi=='y'||lagi=='Y');
   return 0;
}
